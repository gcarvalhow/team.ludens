# Camada `infrastructure/` — Repositórios e Serviços

```
modules/<nome>/infrastructure/
├── repositories/   → persistência do aggregate/entidade
└── services/       → integração com sistema externo (AbacatePay, SMTP...)
```

Nenhuma das duas contém regra de negócio. Repositório busca e salva. Serviço
chama uma API externa e traduz o resultado. A decisão do que fazer com o dado é
sempre do `usecase` (ou do handler de outbox, no caso de serviço externo).

---

## `repositories/`

### A regra: estender antes de reimplementar

`core/infrastructure/repositories/repository.py` já implementa toda operação
genérica: `find_by`, `find_all`, `find_all_by`, `exists_by`, `save` — só isso,
nada mais. Um repositório de módulo **estende** `BaseRepository[T]` ou
`AggregateRepository[T]` e nunca reimplementa esses cinco. Um lookup por id
(`find_by_id`) ou uma trava de linha (`find_by_id_for_update`) **não** vêm de
graça da base — cada repositório especializado implementa o próprio quando um
agregado específico precisa, exatamente como qualquer outro método
não-genérico (ver `references/02`).

```python
# modules/booking/infrastructure/repositories/reservation_repository.py
class ReservationRepository(AggregateRepository[Reservation]):
    model = Reservation

    async def count_open_quantity_for_session(self, session_id: UUID) -> int:
        result = await self._session.execute(
            select(func.coalesce(func.sum(Reservation.quantity), 0)).where(
                Reservation.session_id == session_id,
                Reservation.status == ReservationStatus.OPEN,
                Reservation.expires_at > func.now(),
            )
        )
        return result.scalar_one()
```

- `AggregateRepository[T]` — para aggregate roots que levantam eventos
  (`Reservation`, `Order`, `Show`, `Session`, `User`, `Ticket`).
- `BaseRepository[T]` — para entidades filhas sem lifecycle de eventos próprio.

Só adicione método próprio quando a query não é genérica — agregação, `JOIN`,
`COUNT` condicional (como as contagens que sustentam RN01 e RN05), busca com
lock (`find_by_id_for_update`, criado no repositório do módulo que precisa,
nunca herdado). Antes de escrever, pergunte: é um filtro simples
(`find_all_by`) ou checagem de existência (`exists_by`)? Se for, use o que já
existe na base em vez de reimplementar.

### Sessão é sempre injetada, nunca criada pelo repositório

Todo repositório recebe a `AsyncSession` no construtor. Quem decide os limites da
transação é o usecase. Um repositório nunca abre `session.begin()` nem faz
`commit()`/`rollback()` — só usa a sessão que recebeu. É isso que permite um
usecase compor `SessionRepository` + `TicketRepository` + `ReservationRepository`
numa única transação atômica.

### Anti-padrões

| Errado | Certo |
|---|---|
| Reimplementar `find_by`/`find_all`/`find_all_by`/`exists_by`/`save` num repositório de módulo | Herdar de `BaseRepository` |
| `select(...).with_for_update()` direto num usecase | `repository.find_by_id_for_update(id)`, implementado no próprio repositório do módulo — não herdado de `BaseRepository` |
| Repositório de módulo escrevendo `Event` manualmente | `AggregateRepository.save` já faz isso |
| `DELETE FROM` físico | Soft delete via `is_active=False` por método de domínio |
| Repositório chamando `session.commit()` | Transação é do usecase / `get_db` |

---

## `services/`

`services/` é para integração com sistema externo que não é banco. No Ludens hoje:

- **`PaymentGateway`** (`modules/payment/infrastructure/services/`) — cria a
  cobrança Pix no **AbacatePay** e trata o webhook de confirmação. Cliente HTTP
  assíncrono (`httpx.AsyncClient`).
- **`EmailService`** (`modules/notification/infrastructure/services/`) — envia
  e-mail transacional (confirmação de compra com id/QR do ingresso, recuperação
  de senha). Via SMTP assíncrono.

### O padrão obrigatório para qualquer `services/` novo

```python
class PaymentGatewayError(Exception):
    pass

class PaymentGateway:
    def __init__(self) -> None:
        self._client = httpx.AsyncClient(
            base_url=settings.abacatepay_base_url,
            headers={"Authorization": f"Bearer {settings.abacatepay_api_key}"},
            timeout=httpx.Timeout(10.0),
        )

    async def create_pix_charge(self, order_id: UUID, amount_cents: int) -> PixCharge:
        try:
            resp = await self._client.post("/pixQrCode", json={...})
            resp.raise_for_status()
        except httpx.HTTPError as exc:
            raise PaymentGatewayError("failed to create pix charge") from exc
        return PixCharge.from_api(resp.json())
```

1. **Cliente assíncrono nativo** (`httpx.AsyncClient`, SMTP async) — nunca uma
   lib síncrona chamada direto numa coroutine. Se for síncrona,
   `await asyncio.to_thread(...)`.
2. **Exceção própria do módulo** (`PaymentGatewayError`, `EmailServiceError`),
   nunca a exceção crua da lib subindo até o usecase/router/handler.
3. **Timeout explícito** em toda chamada de rede — RNF03 exige degradação
   graciosa; uma chamada externa pendurada não pode travar o processo.
4. **Credencial de `settings`** (variável de ambiente), nunca hardcoded. Nunca em
   log, nunca em URL.

### Quem consome o serviço externo: o handler de outbox, não o usecase

O usecase que confirma um pagamento levanta `OrderPaid`; o handler registrado
para `OrderPaid` no `notification` chama `EmailService.send_confirmation(...)`.
Se o e-mail falhar, o handler falha e o relay tenta de novo (at-least-once) — a
compra já está confirmada e durável no banco, e **falha de envio de e-mail não
invalida a compra** (RF05). O mesmo vale para estorno no gateway (RF07): o
usecase de cancelamento levanta `OrderRefundRequested`, o handler chama o
AbacatePay.

Exceção: `booking` precisa **criar** a cobrança Pix de forma síncrona no fluxo de
checkout (o comprador vê o QR na hora). Aí o usecase de `payment` chama
`PaymentGateway.create_pix_charge` diretamente, **depois** de já ter salvo o
`Order` com `status=PENDING` — e uma falha aqui deixa o `Order` em `PENDING` com
uma mensagem de erro pro comprador, sem derrubar a transação de domínio.

### `services/` não recebe `AsyncSession`

Um serviço externo não tem noção de transação. A chamada a um serviço externo
nunca deve fazer parte da mesma unidade atômica que o `save` no banco.
