# Camada `api/` e a Fronteira Entre Módulos

Duas coisas neste documento, e a segunda é a regra mais grave do backend: a
anatomia da camada HTTP (`api/routers/`) e o mecanismo que impede o monólito
modular de virar uma bagunça de imports cruzados — `dependencies.py`.

---

## Anatomia de `api/`

```
modules/<nome>/
├── api/routers/<recurso>_router.py   → endpoints (@router.get/post/...)
├── router.py                         → agrega os sub-routers do módulo
└── dependencies.py                   → única porta de entrada pra outros módulos
```

### 1. `api/routers/<recurso>_router.py` — os endpoints

Um `APIRouter` por recurso, com `prefix` e `tags`. O endpoint: recebe request (já
validado pelo schema), resolve dependências via `Depends`, chama o usecase,
devolve o schema de response. **Nunca tem lógica de negócio.**

```python
# modules/booking/api/routers/reservation_router.py
router = APIRouter(prefix="/reservations", tags=["Booking"])

@router.post("", response_model=IdentifierResponse, status_code=201)
async def open_reservation(
    body: OpenReservationRequest,
    session: AsyncSession = Depends(get_db),
    buyer=Depends(get_current_buyer),
):
    return await BookingUseCase(session).open_reservation(body, buyer.id)

@router.post("/{reservation_id}/confirm", status_code=204)
async def confirm(reservation_id: UUID, session: AsyncSession = Depends(get_db), buyer=Depends(get_current_buyer)):
    await BookingUseCase(session).confirm_reservation(reservation_id, buyer.id)
```

Cada rota escolhe a dependência de auth certa: `get_current_buyer` para o
comprador autenticado, `require_admin` para rotas de gestão de espetáculo/sessão
(RF08). Rotas de catálogo público (RF01, RF02) não exigem auth.

### 2. `router.py` — agregador do módulo

```python
# modules/booking/router.py
router = APIRouter()
router.include_router(reservation_router)
```

### 3. `main.py` — só inclui o `router.py` de topo

```python
app.include_router(identity_router)
app.include_router(catalog_router)
app.include_router(booking_router)
app.include_router(payment_router)
# notification não tem router — só handlers de outbox
```

`main.py` nunca importa um `<recurso>_router.py` diretamente, nunca sabe que
`api/routers/` existe.

---

## `dependencies.py` — a única porta de entrada entre módulos

### A regra

**Nenhum módulo importa `domain/` ou `infrastructure/` de outro módulo
diretamente.** Se um módulo precisa de algo de outro, o outro **exporta** uma
função (ou um objeto de dados imutável) no seu `dependencies.py`. Essa é a única
superfície pública entre módulos.

### O que cada módulo exporta

| Módulo | Símbolo | O que resolve |
|---|---|---|
| `identity` | `get_current_user` | Dependency FastAPI — decodifica o Bearer JWT, valida `security_stamp`, carrega o `User`, 401 se inválido/expirado |
| `identity` | `require_admin` | Como acima, mas 403 se `not user.is_admin` (não há enum de papel — `is_admin` é `bool`) |
| `catalog` | `get_session_ref(session, session_id)` | Busca uma `Session` e devolve `SessionRef` (dataclass frozen: `id`, `capacity`, `starts_at`, `is_on_sale`) — nunca o aggregate `Session` inteiro |
| `catalog` | `get_ticket_prices(session, session_id)` | Preços de inteira/meia da sessão, para `payment` calcular o total |
| `payment` | `create_order_for_reservation(...)` | Ponto de entrada de `booking` para abrir a ordem Pix a partir de uma reserva confirmada |

O que atravessa a fronteira nunca é o aggregate completo (que carregaria
`domain/` do outro módulo pro chamador) — é um dataclass frozen com só os campos
que o consumidor precisa:

```python
# modules/catalog/dependencies.py
@dataclass(frozen=True)
class SessionRef:
    id: UUID
    capacity: int
    starts_at: datetime
    is_on_sale: bool

async def get_session_ref(session: AsyncSession, session_id: UUID) -> SessionRef | None:
    s = await SessionRepository(session).find_by("id", session_id)
    if not s:
        return None
    return SessionRef(id=s.id, capacity=s.capacity, starts_at=s.starts_at, is_on_sale=s.is_on_sale)
```

### Código proibido vs. permitido

```python
# ❌ PROIBIDO — booking importando o domain interno de catalog
from app.modules.catalog.domain.aggregates import Session
from app.modules.catalog.infrastructure.repositories import SessionRepository

# ✅ PERMITIDO — via dependência exportada
from app.modules.catalog.dependencies import SessionRef, get_session_ref
```

O primeiro acopla `booking` à estrutura interna de `catalog` — se `catalog` mudar
o schema de `Session`, o import quebra em silêncio noutro módulo. O segundo
acopla `booking` só ao contrato público que `catalog` decidiu manter estável.

> Nota sobre RN05: `booking` precisa travar a linha da `Session`
> (`find_by_id_for_update`) para garantir a disponibilidade atômica. Como
> `booking` não pode importar `SessionRepository` de `catalog`, `catalog` expõe
> em `dependencies.py` um `lock_session_for_update(session, session_id)` que
> devolve o `SessionRef` **depois** de aplicar o `FOR UPDATE` — a trava atravessa
> a fronteira pela porta, não pelo import.

---

## Erros comuns nesta camada

| Erro | Correção |
|---|---|
| Lógica de negócio no handler do router | Mover pro usecase |
| `main.py` importando `<recurso>_router.py` direto | Importar só o `router.py` de topo do módulo |
| Um módulo importando `domain`/`infrastructure` de outro | Pedir (ou criar) dependência exportada em `dependencies.py` |
| Dependência exportada devolvendo o aggregate inteiro de outro módulo | Devolver um tipo próprio da fronteira (`SessionRef`, não `Session`) |
| Rota de gestão (RF08) sem `require_admin` | Toda rota escolhe explicitamente a auth do seu público |
