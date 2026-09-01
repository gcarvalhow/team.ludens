# TEMPLATE — Implementation Spec (Ludens)

O mapa de todo o código a implementar para uma feature, por responsável, com o
passo a passo Trunk-Based Development. Salvar como
`docs.ludens/specs/[domínio]-[conceito]/implementation-spec.md`.

> Pré-condição: `spec.md` (`approved`) e `logic.md` (`reviewed`) da mesma feature.

---

## Frontmatter

```yaml
---
status: draft
spec: [domínio]-[conceito]
created_at: 2026-09-01
---
```

## Cabeçalho

```
# [Nome da feature] — Implementation Spec
```

**Resumo:** 2–3 linhas do que a feature entrega, ponta a ponta.
**RF cobertos:** RFxx · **RN cobertas:** RNxx, RNyy
**Módulo backend:** `booking` · **Feature frontend:** `booking`
**Contrato:** `docs.ludens/specs/[domínio]-[conceito]/integration.md`

---

## A. Backend — responsável: **Igor (Backend)**

> Ordem de dependência obrigatória: `domain/` → `application/` → `infrastructure/`
> → `api/` → `migrations/`. Nunca escrever o router antes do domínio existir.

### A.1 Arquivos a criar / alterar

| # | Camada | Caminho real | O que fazer |
|---|---|---|---|
| 1 | domain | `src/app/modules/<mod>/domain/aggregates/<x>.py` | ... |
| 2 | domain | `src/app/modules/<mod>/domain/events/<x>_events.py` | eventos: `XCreated`, `XExpired`, ... |
| 3 | domain | `src/app/modules/<mod>/domain/enumerations/<x>_status.py` | `str, enum.Enum` |
| 4 | application | `src/app/modules/<mod>/application/schemas/request.py` | Pydantic, só forma |
| 5 | application | `src/app/modules/<mod>/application/schemas/response.py` | nunca expõe aggregate direto |
| 6 | application | `src/app/modules/<mod>/application/usecases/<x>_usecase.py` | orquestra domínio + repo numa transação |
| 7 | infrastructure | `src/app/modules/<mod>/infrastructure/repositories/<x>_repository.py` | estende `AggregateRepository[T]` / `BaseRepository[T]` |
| 8 | infrastructure | `src/app/modules/<mod>/infrastructure/services/<y>.py` | integração externa (AbacatePay/SMTP) — só se aplicável |
| 9 | outbox | `src/app/modules/notification/...` handler + registro no `outbox/registry.py` | handler idempotente por `event_type` |
| 10 | api | `src/app/modules/<mod>/api/routers/<x>_router.py` | endpoint chama usecase, escolhe auth (`get_current_buyer` / `require_admin`) |
| 11 | api | `src/app/modules/<mod>/router.py` | agrega o sub-router |
| 12 | api | `src/app/modules/<mod>/dependencies.py` | só se outro módulo consome algo daqui (retorno = tipo de fronteira, não aggregate) |
| 13 | migration | `migrations/versions/<hash>_<slug>.py` | `alembic revision --autogenerate` + revisar à mão |

### A.2 Código a colar (esqueleto por arquivo)

Para cada arquivo relevante, um bloco de código pronto para colar e completar,
seguindo `backend-architecture` (aggregate muda estado só via
`raise_event`→`_apply`→`_when_*`; usecase orquestra; schema é contrato).

```python
# src/app/modules/<mod>/domain/aggregates/<x>.py
# ... esqueleto real ...
```

### A.3 Onde cada regra de negócio entra

| RN | Onde no código |
|---|---|
| RN05 (disponibilidade atômica) | `<x>_usecase.py` → `repository.find_by_id_for_update(session_id)` antes de decrementar; nunca leitura simples + update |
| RN03 (expiração 15 min) | evento `ReservationExpired` + handler no relay que devolve os ingressos; `OUTBOX_RELAY_INTERVAL_SECONDS` |
| RN01 (6 por CPF) | validação no `<x>_usecase.py` antes de confirmar a reserva |
| RN02 (reembolso por janela) | cálculo puro no domínio (`Order.refund_amount(now)`) |
| RN04 (meia sem documento) | emissão do ingresso **não** exige número de documento de estudante — critério de aceite do teste |

### A.4 Passo a passo TBD (Backend)

```
git checkout master && git pull && git checkout -b feat/<NN>-<slug>
# commit 1 — domínio
git add src/app/modules/<mod>/domain && git commit -m "feat(<mod>): modelar <x> e eventos de domínio"
# commit 2 — application
git add src/app/modules/<mod>/application && git commit -m "feat(<mod>): adicionar usecase e schemas de <x>"
# commit 3 — infrastructure
git add src/app/modules/<mod>/infrastructure && git commit -m "feat(<mod>): repositório e serviço de <x>"
# commit 4 — api + migration
git add src/app/modules/<mod>/api src/app/modules/<mod>/router.py migrations && git commit -m "feat(<mod>): expor rotas de <x> e migration"
```
Depois: `/team-ludens:tbd-pr` → recomenda `senior-dev` (Modo 2) + `/code-review`
→ push → PR com `Closes #<NN>` → merge (1 aprovação + CI verde) →
`/team-ludens:tbd-pr` de novo finaliza o ciclo.

---

## B. Frontend — responsável: **Diego (Frontend)**

> Ordem de dependência: `routes/endpoints.js` → `schemas/` → `services/` →
> `hooks/queries/query-options.js` + `hooks/queries/` → `hooks/mutations/` →
> `hooks/forms/` → `components/` → `components/ui/` → barrels.

### B.1 Arquivos a criar / alterar

| # | Camada | Caminho real | O que fazer |
|---|---|---|---|
| 1 | endpoints | `src/routes/endpoints.js` | adicionar o grupo da feature; rotas parametrizadas são funções |
| 2 | schemas | `src/features/<feat>/schemas/<x>.schema.js` | Zod — response schema + DTO de request |
| 3 | services | `src/features/<feat>/services/<x>.service.js` | `fetcher` + `endpoints` + `.parse()`; transform de shape aqui, não no componente |
| 4 | queries | `src/features/<feat>/hooks/queries/query-options.js` | query keys + query options centralizados |
| 5 | queries | `src/features/<feat>/hooks/queries/use<X>Queries.js` | `useQuery` sobre as options |
| 6 | mutations | `src/features/<feat>/hooks/mutations/use<X>Mutations.js` | `useMutation` → invalida queries + toast sucesso + toast erro |
| 7 | forms | `src/features/<feat>/hooks/forms/use<X>Form.js` | `react-hook-form` + resolver Zod (schema de request) — só se houver form |
| 8 | components | `src/features/<feat>/components/<X>.jsx` | conecta hooks e UI; trata loading/error/empty |
| 9 | components/ui | `src/features/<feat>/components/ui/<X>.jsx` | apresentacional puro — sem `useQuery`/`useMutation`/service |
| 10 | barrels | `index.js` em toda subpasta criada + na raiz da feature | obrigatório, não é dívida |

### B.2 Código a colar (esqueleto por arquivo)

Blocos prontos seguindo `frontend-architecture` (fonte de tipo = schema Zod;
`query-options.js` obrigatório; toda mutation invalida + toast; `components/ui`
nunca fala com service).

### B.3 Contrato consumido

Aponta `docs.ludens/specs/[domínio]-[conceito]/integration.md`. Enquanto o
backend não implementou, o frontend trabalha contra o **contrato-alvo** desse
arquivo; ao integrar de verdade, se o shape divergir, o ajuste é um transform na
service layer + registro da divergência — nunca editar o repo de backend.

### B.4 Passo a passo TBD (Frontend)

```
git checkout master && git pull && git checkout -b feat/<NN>-<slug>
# commit 1 — contrato
git add src/routes/endpoints.js src/features/<feat>/schemas src/features/<feat>/services && git commit -m "feat(<feat>): endpoints, schemas e services de <x>"
# commit 2 — hooks
git add src/features/<feat>/hooks && git commit -m "feat(<feat>): queries e mutations de <x>"
# commit 3 — UI
git add src/features/<feat>/components && git commit -m "feat(<feat>): telas e componentes de <x>"
# commit 4 — barrels
git add src/features/<feat> && git commit -m "chore(<feat>): barrels index.js da feature <x>"
```
Depois: `npm run lint && npm run build` verdes → `/team-ludens:tbd-pr`.

---

## C. QA — responsável: **Adrian (QA)**

### C.1 Definition of Ready — checagem

Confirmar item a item (`docs.ludens/team/quality.md`). Apontar o que falta.

### C.2 Casos de teste de domínio (pytest) — a colar

| Caso | Cenário (estado → ação → asserção) | RN |
|---|---|---|
| ... | ... | ... |

```python
# tests/modules/<mod>/test_<x>.py
# ... casos prontos ...
```

### C.3 Roteiro de teste manual pré-entrega

`busca do espetáculo → seleção da sessão e do ingresso → reserva → pagamento →
confirmação` + casos obrigatórios (preço inteira/meia; expiração devolve
ingressos; duas compras concorrentes não excedem capacidade; falha de pagamento
libera reserva; limite por CPF) + teste de resiliência (derrubar gateway/e-mail)
+ teste de restart com reservas abertas.

### C.4 Passo a passo TBD (QA)

```
git checkout master && git pull && git checkout -b test/<NN>-<slug>
git add tests/modules/<mod> && git commit -m "test(<mod>): cobrir <regras> de <x>"
```

---

## D. DevOps — responsável: **Gabriel (DevOps)** — *só se aplicável*

- Variáveis novas em `.env.example` (com classificação `SECRET`/`SENSITIVE`/`CONFIG`)
- Segredos no pipeline de CI
- Ajuste de workflow, se necessário

---

## E. Ordem entre as fatias

Backend e QA (casos de domínio) podem começar juntos a partir do `logic.md`.
Frontend começa em paralelo contra o contrato-alvo do `integration.md`. A
integração real (frontend consumindo o backend implementado) e o `integration.md`
canônico só depois do merge do backend.

## F. Bloqueios em aberto

Liste aqui qualquer `[bloqueio: decidir antes de implementar]` herdado das
perguntas abertas do `spec.md`/`logic.md`. Nenhuma fatia com bloqueio aberto
deve ser fatiada em issue antes da decisão.
