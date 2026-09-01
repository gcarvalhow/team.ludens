# Outbox e o Fluxo Completo de Eventos

Este é o documento mais importante pra entender Event-Driven Architecture neste
backend. O Ludens usa um **Outbox in-process** — sem broker. ADR:
`docs.ludens/backend/design/001-outbox-in-process.md`.

Por que Outbox, em uma frase: gravar o `Event` na mesma transação SQL que a
mudança de domínio troca uma transação distribuída (mudar estado + disparar
e-mail/estorno, impossível de garantir atomicamente) por uma transação local +
processo assíncrono de entrega.

---

## A tabela `events`

```python
# outbox/models.py
class Event(Model):
    __tablename__ = "events"

    aggregate_id: Mapped[UUID] = mapped_column(nullable=False, index=True)
    event_type: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    payload: Mapped[dict] = mapped_column(JSONB, nullable=False)
    dispatched_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
```

- **`aggregate_id`** — id do aggregate que originou o evento. Não é FK — a tabela
  `events` é desacoplada de qualquer tabela de domínio de propósito.
- **`event_type`** — nome da classe do evento (`"OrderPaid"`, `"ReservationExpired"`).
- **`payload`** — o evento serializado para JSONB. `AggregateRepository._serialize`
  converte `UUID`/`datetime`/etc. para string.
- **`dispatched_at`** — `NULL` = ainda não processado. Preenchido = os handlers já
  rodaram com sucesso. Nunca é reescrito de volta para `NULL`.

Nenhum módulo escreve em `events` diretamente. A única via é
`AggregateRepository.save`, que drena `entity.dequeue_events()` e grava uma linha
por evento, na mesma transação SQL do `save` do aggregate.

---

## O `OutboxRelay` — in-process, sem broker

`src/app/outbox/relay.py`, subido como `asyncio.Task` de background pelo
`lifespan` de `main.py`:

```python
@asynccontextmanager
async def lifespan(app: FastAPI):
    task = asyncio.create_task(run_outbox_relay())
    yield
    task.cancel()
```

O loop:

1. A cada iteração, abre uma transação (`session.begin()`).
2. Busca até **50** `Event` com `dispatched_at IS NULL`, ordenados por
   `created_at`.
3. Para cada evento: procura os handlers registrados para `event.event_type` no
   **registry in-process** e chama cada um `await handler(event_payload)`. Se
   todos tiverem sucesso, seta `event.dispatched_at = now()`.
4. A transação inteira (SELECT + todos os UPDATEs de `dispatched_at`) fecha junto.
5. `await asyncio.sleep(OUTBOX_RELAY_INTERVAL_SECONDS)` (padrão **2s**).
6. Uma exceção num handler é logada; o `dispatched_at` daquele evento **não** é
   marcado — na próxima volta ele é reprocessado (at-least-once).

### O registry

```python
# outbox/registry.py
_handlers: dict[str, list[Callable]] = defaultdict(list)

def register(event_type: str):
    def deco(fn):
        _handlers[event_type].append(fn)
        return fn
    return deco

def handlers_for(event_type: str) -> list[Callable]:
    return _handlers[event_type]
```

Cada módulo registra seus handlers no import (`main.py` importa
`modules.notification.handlers` etc. no boot):

```python
# modules/notification/handlers.py
@register("OrderPaid")
async def send_purchase_confirmation(payload: dict) -> None:
    # idempotente: se o e-mail para este order_id já foi enviado, retorna sem repetir
    ...

@register("ReservationExpired")
async def return_seats_to_availability(payload: dict) -> None:
    # já é coberto pelo domínio via evento; handler aqui só se houver efeito externo
    ...
```

---

## Garantia at-least-once — handlers idempotentes

Se o relay morrer **depois** de um handler ter efeito externo (e-mail enviado)
mas **antes** de commitar o `dispatched_at`, o evento continua `NULL` e é
reprocessado — o handler roda de novo. Não há trava contra isso: é a escolha
deliberada de at-least-once. **Todo handler precisa ser idempotente** —
processar o mesmo `OrderPaid` duas vezes não pode enviar dois e-mails nem
estornar duas vezes. A forma prática: cada handler checa um marcador ("já
enviei confirmação para este order_id?") antes de agir.

## Latência esperada

Entre o commit da transação de domínio e o efeito do handler: **até ~2 segundos**
(o intervalo do relay). Não é tempo real. RF05 dá 5 minutos de folga para o
e-mail de confirmação — ~2s cabe com sobra. Nenhuma feature pode assumir entrega
instantânea.

## Recuperação de estado após restart

O relay morre junto com o processo da API. Ao subir de novo, ele volta a fazer
polling e **eventos com `dispatched_at IS NULL` continuam sendo processados** —
nada se perde. Isso é o que sustenta RNF03: depois de um restart, reservas
expiradas continuam sendo devolvidas e nenhuma compra paga se perde, porque **o
banco é a fonte de verdade, não a memória do processo**. Migrar o relay para um
processo separado ou para um broker no futuro não muda nenhum contrato — a tabela
`events` é o ponto de extensão.

## O ciclo completo: checkout → pagamento → confirmação

1. **`POST /reservations`** (`BookingUseCase.open_reservation`, `get_current_buyer`)
   — trava a `Session` (`find_by_id_for_update`), valida RN01 e RN05, grava
   `Reservation` (`status=OPEN`, `expires_at = now + 15min`) via
   `AggregateRepository` — que grava também o `Event` `ReservationOpened`.
2. **`POST /reservations/{id}/confirm`** → `PaymentUseCase.create_order` abre um
   `Order` (`status=PENDING`) e chama `PaymentGateway.create_pix_charge`
   **síncrono** (o comprador vê o QR). Evento `OrderCreated`.
3. **Webhook do AbacatePay** (`POST /payments/webhook`) → `PaymentUseCase.mark_paid`
   → `order.mark_paid()` + `reservation.confirm()` + emissão dos `Ticket` (id
   único / QR) na mesma transação. Evento `OrderPaid`.
4. **`OutboxRelay`** pega `OrderPaid` no próximo ciclo (~2s) e chama os handlers
   registrados: `notification` envia o e-mail de confirmação com os ingressos.
5. Se o pagamento **falhar** ou expirar: `order.mark_failed()` +
   `reservation.expire()` **libera a reserva imediatamente** (RF04), e os
   ingressos voltam à disponibilidade da sessão.
6. Reservas `OPEN` cujo `expires_at` passou são varridas por um job leve do
   próprio relay (ou um segundo `asyncio.Task`) que chama `reservation.expire()`
   — RN03.

---

## Anti-padrões

| Errado | Certo |
|---|---|
| `await email_service.send(...)` chamado de dentro de um usecase | `aggregate.raise_event(OrderPaid(...))` + `repository.save` — o envio real só acontece num handler de outbox |
| Handler que trata reprocessar o mesmo evento como bug | At-least-once é o contrato — o handler precisa ser idempotente |
| Depender de latência sub-segundo pra um fluxo novo | ~2s é o piso; latência menor é decisão de arquitetura, não ajuste de `sleep` |
| Chamar o AbacatePay/estorno direto no usecase de cancelamento | Levantar `OrderRefundRequested`; o handler chama o gateway |

## Regra final — não negociável

Nenhum efeito colateral externo (e-mail, estorno, webhook de terceiro) pode pular
o Outbox. Não existe "só dessa vez chama direto". Se o efeito importa, ele nasce
de um `Event` gravado na mesma transação do usecase, e a via é sempre salvar o
aggregate via `AggregateRepository`. Exceção única e explícita: a **criação** da
cobrança Pix no checkout, que é síncrona por necessidade de produto (o QR na
tela) e acontece sempre depois do `Order` já estar salvo.
