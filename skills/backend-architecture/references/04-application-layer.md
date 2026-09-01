# A Camada `application/`

## Objetivo

`application/` é onde domínio e infraestrutura se encontram, dentro dos limites de
uma transação de banco. Cada módulo tem:

```
application/
├── usecases/    # orquestra domínio + infraestrutura numa transação
└── schemas/     # contratos de I/O da API — request.py / response.py
```

Regra que este documento deixa inequívoca: **usecase orquestra, aggregate decide,
schema é contrato.**

---

## `usecases/` — orquestração dentro de uma transação

Um usecase recebe uma `AsyncSession` no `__init__`, monta os repositórios que
precisa, e expõe métodos que representam um caso de uso completo. A transação já
está em andamento quando o método é chamado, porque `get_db()`
(`src/app/dependencies.py`) envolve toda a request num `async with session.begin()`:

```python
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        async with session.begin():
            yield session
```

Tudo que um método de usecase faz com a sessão — ler, mutar aggregates, chamar
`repository.save()` várias vezes — faz parte da mesma transação, e só vira
`COMMIT` quando a request termina sem exceção.

### Exemplo: `BookingUseCase.open_reservation` — o coração da RN05

```python
async def open_reservation(self, request: OpenReservationRequest, buyer_id: UUID) -> IdentifierResponse:
    # 1. trava a linha da sessão — nada de leitura simples
    session = await self._session_repo.find_by_id_for_update(request.session_id)
    if session is None or not session.is_on_sale:
        raise DomainError("session not available")

    # 2. regra cruzando dados persistidos: limite por CPF (RN01)
    already = await self._ticket_repo.count_for_buyer_in_session(buyer_id, session.id)
    if already + request.quantity > MAX_TICKETS_PER_CPF:
        raise DomainError("ticket limit per CPF exceeded")

    # 3. disponibilidade atômica (RN05): a linha da sessão está travada,
    #    ninguém mais consegue reservar em paralelo até esta transação fechar
    sold = await self._ticket_repo.count_confirmed_for_session(session.id)
    held = await self._reservation_repo.count_open_quantity_for_session(session.id)
    if sold + held + request.quantity > session.capacity:
        raise DomainError("not enough seats available")

    reservation = Reservation.open(buyer_id, session.id, request.quantity, ttl_minutes=RESERVATION_TTL_MINUTES)
    await self._reservation_repo.save(reservation)
    return IdentifierResponse(id=reservation.id)
```

Por que a validação de capacidade vive no usecase e não em `Reservation.open()`:
para saber quantos ingressos já estão vendidos/segurados na sessão, o usecase
precisa ler outros aggregates (`Session`, `Ticket`) e contar linhas.
`Reservation.open()` não tem — e não deveria ter — acesso a repositório. O
aggregate só sabe construir a si mesmo e levantar `ReservationOpened`.

O `find_by_id_for_update` na linha 1 é o que torna os passos 2–3 corretos sob
concorrência: enquanto esta transação não fecha, nenhuma outra transação
consegue travar a mesma `Session`, então a contagem "vendidos + segurados +
pedido" não pode ser corrida por uma segunda compra.

### Regra: usecase não é dono de regra de negócio pura

| Errado | Certo |
|---|---|
| `if reservation.status == OPEN: reservation.status = CONFIRMED` no usecase | `reservation.confirm()` |
| Cálculo de reembolso (RN02) espalhado em vários usecases | `order.refund_amount(session_starts_at, now)` — regra pura de `Order` |
| Usecase decidindo `ticket.type = HALF` direto | Método do aggregate |

Critério: se a regra pode ser expressa e testada **sem tocar em outro aggregate
nem em infraestrutura**, ela pertence ao aggregate. Se só existe porque depende de
ler outro aggregate, contar linhas ou chamar um serviço externo, é orquestração e
fica no usecase.

### Efeitos colaterais externos nunca são chamados no usecase

O usecase **não** chama o gateway de pagamento nem o serviço de e-mail
diretamente. Ele levanta um evento de domínio (`OrderPaymentRequested`,
`OrderPaid`) e salva o aggregate — o handler de outbox (`references/07`) é quem
chama o AbacatePay ou o SMTP, fora da transação, de forma idempotente. Exceção:
uma leitura síncrona best-effort que não muda estado (raro) pode ficar no
usecase, sempre depois do `save`, com a falha só logada.

---

## `schemas/` — contrato de I/O, nunca o domínio exposto direto

Cada módulo separa `request.py` (o que a API aceita) de `response.py` (o que a
API devolve). **Nenhum router ou usecase devolve um objeto de domínio direto pela
API** — sempre passa por um schema Pydantic explícito.

```python
# booking/application/schemas/request.py
class OpenReservationRequest(BaseModel):
    session_id: UUID
    quantity: int = Field(ge=1, le=6)   # forma; o teto real por CPF é regra de negócio no usecase
    ticket_type: TicketType

# booking/application/schemas/response.py
class ReservationResponse(BaseModel):
    id: UUID
    session_id: UUID
    quantity: int
    status: ReservationStatus
    expires_at: datetime
```

| Proibido | Permitido |
|---|---|
| `return reservation` num router tipado `-> Reservation` | `return self._to_response(reservation)` retornando `ReservationResponse` |
| Validação de negócio no schema ("sessão esgotada") | Schema valida só forma (`Field(ge=1)`, regex de CPF); "esgotada" é estado persistido, vai no usecase |
| Um campo `Any` que "passa o aggregate inteiro" | Campos explícitos, tipados, um a um |

---

## Resumo operacional

- `usecases/`: único lugar que mistura leitura/escrita de múltiplos repositórios
  e decide quais métodos de domínio chamar, sempre dentro da transação de
  `get_db()`. Opera `find_by_id_for_update` em toda operação de disponibilidade.
- `aggregates/` (domínio): dono da regra pura — tudo que pode ser decidido só com
  o próprio estado.
- `schemas/`: contrato de I/O — nunca expõe domínio direto, nunca decide regra de
  negócio, só valida forma e formata resposta.
