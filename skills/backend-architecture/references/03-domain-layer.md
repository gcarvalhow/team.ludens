# A Camada `domain/`

## Objetivo

`domain/` é onde vive a regra de negócio de cada módulo. É a camada que não sabe
que FastAPI, SQLAlchemy-como-ORM-de-request ou o gateway de pagamento existem —
sabe apenas o que é uma `Reservation`, o que é um `Order`, e quais transições de
estado são válidas. Todo módulo tem a mesma estrutura interna:

```
domain/
├── aggregates/      # raiz do agregado — identidade + invariantes + comportamento
├── entities/        # entidade filha, sem identidade própria fora do agregado
├── value_objects/   # tipos imutáveis sem identidade (ex.: CPF, Money)
├── enumerations/    # vocabulário fechado do domínio
└── events/          # eventos de domínio que o aggregate levanta
```

Regra central: **estado de aggregate nunca muda por atribuição direta de campo
por fora dele.** Toda mudança passa por um método do próprio aggregate.

---

## `aggregates/` — a raiz com invariantes e comportamento

Um aggregate root herda de `AggregateRoot` (`core/domain/aggregate.py`) e de
`Model` (`core/domain/model.py`). Exemplo com `Reservation`
(`src/app/modules/booking/domain/aggregates/reservation.py`):

```python
class Reservation(AggregateRoot, Model):
    __tablename__ = "reservations"

    buyer_id: Mapped[UUID] = mapped_column(nullable=False)
    session_id: Mapped[UUID] = mapped_column(nullable=False)
    quantity: Mapped[int] = mapped_column(nullable=False)
    status: Mapped[ReservationStatus] = mapped_column(nullable=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    @classmethod
    def open(cls, buyer_id: UUID, session_id: UUID, quantity: int, ttl_minutes: int) -> "Reservation":
        reservation = cls()
        now = datetime.now(timezone.utc)
        reservation.raise_event(lambda v: ReservationOpened(
            version=v, id=reservation.id, buyer_id=buyer_id, session_id=session_id,
            quantity=quantity, expires_at=now + timedelta(minutes=ttl_minutes),
        ))
        return reservation

    def confirm(self) -> None:
        if self.status is not ReservationStatus.OPEN:
            raise DomainError("reservation is not open")
        self.raise_event(lambda v: ReservationConfirmed(version=v, id=self.id, session_id=self.session_id))

    def expire(self) -> None:
        if self.status is not ReservationStatus.OPEN:
            return
        self.raise_event(lambda v: ReservationExpired(
            version=v, id=self.id, session_id=self.session_id,
            quantity=self.quantity, expired_at=datetime.now(timezone.utc),
        ))

    def _when_ReservationOpened(self, e: ReservationOpened) -> None:
        self.buyer_id, self.session_id = e.buyer_id, e.session_id
        self.quantity, self.expires_at = e.quantity, e.expires_at
        self.status = ReservationStatus.OPEN

    def _when_ReservationConfirmed(self, e: ReservationConfirmed) -> None:
        self.status = ReservationStatus.CONFIRMED

    def _when_ReservationExpired(self, e: ReservationExpired) -> None:
        self.status = ReservationStatus.EXPIRED
```

Não existe nenhum lugar em `Reservation` que faça `self.status = ...` fora de um
handler `_when_*`. Um método público (`confirm`, `expire`) valida o invariante
interno e levanta o evento — é o `_apply` (dentro de `raise_event`) que aplica a
mudança. Assim **todo** estado que o aggregate carrega tem, por construção, um
evento correspondente.

### O que fica no aggregate vs. no usecase

`Reservation.confirm()` **não** verifica se ainda há capacidade na sessão — isso
depende de ler outro aggregate (`Session`) e travar a linha dele
(`find_by_id_for_update`), o que acontece **antes**, no usecase (`references/04`).
O que o aggregate garante é o próprio invariante: só confirma se estiver `OPEN`, e
a transição + o evento saem sempre juntos.

O cálculo de reembolso de `Order` (RN02: ≥48h total, 48–24h 50%, <24h nada) **é**
regra pura de domínio — depende só do estado do `Order` e do horário da sessão,
sem tocar outro aggregate nem infra:

```python
def refund_amount(self, session_starts_at: datetime, now: datetime) -> Money:
    hours = (session_starts_at - now).total_seconds() / 3600
    if hours >= 48:
        return self.total
    if hours >= 24:
        return self.total * 0.5
    return Money.zero()
```

### Regra central

| Proibido | Permitido |
|---|---|
| `reservation.status = ReservationStatus.CONFIRMED` fora de `Reservation` | `reservation.confirm()` |
| `order.status = OrderStatus.PAID` num usecase | `order.mark_paid(...)` |
| Construir `ReservationExpired(...)` solto num usecase só pra "logar" | `reservation.expire()`, que chama `raise_event` |

---

## `entities/` — entidade filha, não aggregate root

Uma entidade filha herda só de `Model` — **não** de `AggregateRoot`. Não tem
identidade que faça sentido fora do dono, não levanta eventos próprios, não tem
`raise_event`/`_apply`. Quem cria e muta é sempre o aggregate root dono, nos
handlers `_when_*`. O repositório de uma entidade filha estende
`BaseRepository[T]`, nunca `AggregateRepository[T]`, e serve só para leitura fora
do agregado.

Antes de dar a uma entidade filha (a) repositório de escrita próprio, (b)
capacidade de levantar eventos, ou (c) usecase dedicado a mutá-la, pergunte: **ela
deveria deixar de ser filha e virar aggregate root?** Se não — porque não tem
ciclo de vida independente — ela continua sendo mutada só pelo aggregate dono.

---

## `value_objects/`, `enumerations/`, `events/`

### `value_objects/`

Tipo imutável sem identidade, com validação embutida. Exemplos no Ludens: `CPF`
(valida dígitos verificadores — RF09), `Money` (evita float em preço), `Email`.

```python
@dataclass(frozen=True)
class CPF:
    value: str
    def __post_init__(self):
        if not _is_valid_cpf(self.value):
            raise DomainError("invalid CPF")
```

### `enumerations/`

Vocabulário fechado do módulo, sempre `str, enum.Enum`:

```python
class ReservationStatus(str, enum.Enum):
    OPEN = "open"
    CONFIRMED = "confirmed"
    EXPIRED = "expired"
    CANCELLED = "cancelled"

class OrderStatus(str, enum.Enum):
    PENDING = "pending"
    PAID = "paid"
    FAILED = "failed"
    REFUNDED = "refunded"

class TicketType(str, enum.Enum):
    FULL = "full"
    HALF = "half"
```

### `events/`

Cada evento é um `@dataclass(frozen=True)` que estende `DomainEvent`. Um evento
novo corresponde exatamente a uma linha `Event` inserida na tabela de outbox **na
mesma transação** que persiste o aggregate, via `AggregateRepository.save()`.
Construir um evento manualmente num usecase, fora de `raise_event`, não gera
outbox nenhum e é sempre incorreto.

---

## Anti-padrões da camada `domain/`

| Proibido | Permitido |
|---|---|
| `order.status = OrderStatus.PAID` fora de `Order` | `order.mark_paid(...)` |
| `ReservationConfirmed(version=1, ...)` construído solto | `reservation.confirm()`, que chama `raise_event` |
| `httpx.post(gateway_url, ...)` chamado de um handler `_when_*` ou de um método de aggregate | O aggregate só levanta o evento; quem chama o gateway é um handler de outbox, fora de `domain/` |
| Um usecase setando `ticket.type` direto | Método do aggregate dono que levanta evento e aplica no `_when_*` |
| Repositório de entidade filha estendendo `AggregateRepository` | `BaseRepository`, leitura sem lifecycle próprio |
