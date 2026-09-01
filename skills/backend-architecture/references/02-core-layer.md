# A Camada `core/`

## Objetivo

`src/app/core/` é o único lugar do backend onde é permitido escrever código sem
dono de módulo. Tudo aqui precisa servir 2+ módulos (`identity`, `catalog`,
`booking`, `payment`, `notification`) **sem carregar opinião de domínio de
nenhum deles**. `core/` não sabe o que é uma `Session`, uma `Reservation` ou um
`Ticket` — só sabe o que é um aggregate, uma entidade persistida e um
repositório genérico.

```
core/
├── domain/
│   ├── model.py       # Model (DeclarativeBase) — toda tabela herda daqui
│   ├── aggregate.py   # AggregateRoot — mixin de quem levanta eventos
│   ├── events.py      # DomainEvent base + Protocols
│   └── errors.py      # DomainError — violação de invariante, traduzida a HTTP pela API
└── infrastructure/repositories/
    └── repository.py  # BaseRepository[T] e AggregateRepository[T]
```

Se a primeira frase que descreve o que você fez em `core/` menciona `Show`,
`Session`, `Reservation`, `Order`, `Ticket` ou `Buyer` por nome, esse código está
no lugar errado.

---

## `core/domain/model.py` — `Model`

Toda tabela herda de `Model`, que fixa quatro colunas para qualquer entidade:

```python
class Model(DeclarativeBase):
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
```

### Soft delete via `is_active` — regra, não convenção

Nenhuma linha é fisicamente apagada. "Deletar" um `Show` significa marcar
`is_active = False` por um método de domínio (`Show.deactivate()`), nunca um
`DELETE FROM` nem `session.delete(entity)`. Toda leitura de `BaseRepository` já
filtra `is_active == True` por padrão — uma linha desativada desaparece de
qualquer query genérica automaticamente.

Regra de produto correlata (RF08): uma sessão **com ingressos vendidos** não pode
ser deletada, só **cancelada** — o que dispara o fluxo de reembolso (RF07). O
"cancelada" é um estado de domínio da `Session`, não um `is_active = False`.

| Proibido | Permitido |
|---|---|
| `await session.delete(show)` | `show.deactivate()` + `repository.save(show)` |
| `DELETE FROM shows WHERE id = ...` | método de domínio que seta `is_active = False` via evento |

---

## `core/domain/aggregate.py` — `AggregateRoot`

Mixin que dá a qualquer aggregate root a capacidade de acumular eventos de
domínio antes de persistir:

```python
class AggregateRoot:
    def __init__(self) -> None:
        self._version: int = 0
        self._events: deque[DomainEvent] = deque()

    def raise_event(self, factory: Callable[[int], DomainEvent]) -> None:
        self._version += 1
        event = factory(self._version)
        self._apply(event)
        self._events.append(event)

    def dequeue_events(self) -> list[DomainEvent]:
        events, self._events = list(self._events), deque()
        return events

    def _apply(self, event: DomainEvent) -> None:
        handler = getattr(self, f"_when_{type(event).__name__}", None)
        if handler:
            handler(event)
```

Fluxo, em qualquer aggregate do sistema:

1. Um método de domínio (`Reservation.confirm()`, `Order.mark_paid()`) chama
   `self.raise_event(lambda v: AlgumEvento(version=v, ...))`.
2. `raise_event` incrementa a versão, constrói o evento, chama `_apply` (que
   dispara `_when_<Evento>`, mudando os campos do aggregate) e empilha o evento.
3. Quando o repositório salva o aggregate, ele chama `dequeue_events()` — a lista
   vira linhas `Event` na tabela de outbox.

### Aggregate root vs. entidade comum

`AggregateRoot` **não** é herdado por toda classe com tabela — só pela raiz do
agregado. Aggregates do Ludens: `Buyer` (`identity`), `Show` e `Session`
(`catalog`), `Reservation` e `Ticket` (`booking`), `Order` (`payment`). Uma
entidade filha (ex.: um item de reserva dentro de `Reservation`, se existir)
herda só de `Model` — não levanta eventos por conta própria; quem muda o estado
dela é o aggregate root dono, nos handlers `_when_*`. Ver `references/03`.

---

## `core/domain/events.py` — `DomainEvent`

```python
@dataclass(frozen=True)
class DomainEvent:
    version: int
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
```

Todo evento de módulo estende `DomainEvent` — sempre `@dataclass(frozen=True)`,
sempre com `version` e `timestamp`, mais os campos que descrevem o que mudou:

```python
@dataclass(frozen=True)
class ReservationExpired(DomainEvent):
    id: UUID = field(kw_only=True)
    session_id: UUID = field(kw_only=True)
    quantity: int = field(kw_only=True)
    expired_at: datetime = field(kw_only=True)
```

`core/` nunca conhece o nome de um evento específico.

---

## `core/domain/errors.py` — `DomainError`

Violação de invariante de domínio levanta `DomainError` (ou subclasse). A camada
de API traduz para o status HTTP certo (ex.: `422` para regra de negócio, `409`
para conflito de concorrência). O domínio nunca importa `HTTPException`.

---

## `core/infrastructure/repositories/repository.py`

### `BaseRepository[T]` — CRUD genérico

```python
class BaseRepository(Generic[T]):
    model: ClassVar[type]

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def find_by_id(self, entity_id: UUID) -> T | None: ...
    async def find_by(self, field: str, value: Any) -> T | None: ...
    async def find_all_by(self, *, order_by=None, **filters: Any) -> list[T]: ...
    async def find_by_id_for_update(self, entity_id: UUID) -> T | None: ...   # SELECT ... FOR UPDATE
    async def exists_by(self, field: str, value: Any) -> bool: ...

    async def save(self, entity: T) -> None:
        self._session.add(entity)
```

Toda leitura genérica já inclui `self.model.is_active == True` no `WHERE`.

### `AggregateRepository[T]` — drena eventos para o outbox

```python
class AggregateRepository(BaseRepository[T]):
    async def save(self, entity: T) -> None:
        self._session.add(entity)
        for event in entity.dequeue_events():
            self._session.add(Event(
                aggregate_id=entity.id,
                event_type=event.__class__.__name__,
                payload=self._serialize(event),
            ))
```

`session.add(entity)` e `session.add(Event(...))` acontecem na mesma chamada de
`save`, dentro da mesma `AsyncSession` → os dois `INSERT`s fazem parte da **mesma
transação**. Se o commit falhar, nenhum dos dois vai; se tiver sucesso, os dois
vão juntos. É essa propriedade que sustenta o Outbox (`references/07`).

`AggregateRepository[T]` — para aggregate roots que levantam eventos.
`BaseRepository[T]` — para entidades filhas sem lifecycle próprio.

### `find_by_id_for_update` — obrigatório em toda operação de "reservar"

Qualquer fluxo que reivindica ou muta disponibilidade de assento (reservar,
confirmar, liberar, cancelar) usa `find_by_id_for_update` para travar a linha da
`Session` antes de recontar/decrementar — nunca leitura simples seguida de
update. Esse é o mecanismo concreto de RN05. Duas requests reservando a última
poltrona ao mesmo tempo é exatamente o cenário que isso evita.

---

## O que NUNCA vai em `core/`

| Nunca | Motivo |
|---|---|
| Um enum como `ReservationStatus`, `OrderStatus` | Vocabulário de um módulo — vive em `modules/<nome>/domain/enumerations/` |
| "reserva não pode exceder 6 ingressos por CPF" (RN01) | Invariante/regra de um aggregate ou usecase específico |
| Cálculo de reembolso por janela (RN02) | Regra de `Order`, no domínio de `payment` |
| Contagem de ingressos vendidos por sessão | Depende de conhecer `Ticket`/`Session` — fica no repositório de `booking`/`catalog` |

Teste rápido: se a assinatura do método ou o nome da classe precisa citar um
conceito de módulo para fazer sentido, não é `core/`.
