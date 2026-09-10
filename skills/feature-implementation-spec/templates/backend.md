# TEMPLATE — `backend.md` (Ludens)

Todo o código de backend de uma feature, arquivo a arquivo, pronto para colar.
Salvar como `docs.ludens/specs/[domínio]-[conceito]/backend.md`.

> Pré-condição: `spec.md` (`approved`) e `logic.md` (`reviewed`) da mesma feature.
> Regra de ouro: **nenhum bloco de código com `...` ou `# TODO`** — conteúdo
> inteiro do arquivo, sempre.

---

## Frontmatter

```yaml
---
status: draft
spec: [domínio]-[conceito]
surface: backend
created_at: AAAA-MM-DD
---
```

## Cabeçalho (igual nos três documentos)

```
# [Nome da feature] — Backend
```

**Resumo:** 2–3 linhas do que a feature entrega, ponta a ponta.
**RF:** RFxx · **RN:** RNxx, RNyy · **Módulo backend:** `booking`
**Contrato:** `docs.ludens/specs/[domínio]-[conceito]/integration.md`
**Carregar antes:** skill `backend-architecture` (todos os `references/`),
`docs.ludens/backend/overview.md`.

---

## 1. Arquivos (ordem de dependência)

| # | Camada | Caminho | Novo/Editar |
|---|---|---|---|
| 1 | domain | `src/app/modules/<mod>/domain/value_objects/<x>.py` | novo |
| 2 | domain | `src/app/modules/<mod>/domain/enumerations/<x>.py` | novo |
| 3 | domain | `src/app/modules/<mod>/domain/aggregates/<x>.py` | novo |
| 4 | domain | `src/app/modules/<mod>/domain/events/<mod>_events.py` | novo |
| 5 | application | `src/app/modules/<mod>/application/schemas/request.py` | novo |
| 6 | application | `src/app/modules/<mod>/application/schemas/response.py` | novo |
| 7 | application | `src/app/modules/<mod>/application/usecases/<x>_usecase.py` | novo |
| 8 | infrastructure | `src/app/modules/<mod>/infrastructure/repositories/<x>_repository.py` | novo |
| 9 | infrastructure | `src/app/modules/<mod>/infrastructure/services/<y>.py` | novo — só se houver integração externa |
| 10 | outbox | `src/app/modules/<mod>/handlers.py` + `src/app/outbox/registry.py` | novo / editar |
| 11 | api | `src/app/modules/<mod>/api/routers/<x>_router.py` | novo |
| 12 | api | `src/app/modules/<mod>/router.py` | novo/editar |
| 13 | api | `src/app/modules/<mod>/dependencies.py` | novo — só se outro módulo consome algo |
| 14 | migration | `migrations/versions/<hash>_<slug>.py` | novo |
| 15 | config | `src/app/config.py` + `.env.example` | editar — só se houver variável nova |

## 2. Código

Para **cada** arquivo da tabela, um bloco assim (conteúdo inteiro):

```python
# src/app/modules/<mod>/domain/aggregates/<x>.py  — novo
from __future__ import annotations
# ... arquivo completo, sem elipses ...
```

Arquivo que já existe e só recebe um trecho: mostrar a função/classe nova
inteira, com os imports que ela exige, e uma linha dizendo onde encaixa
(ex.: "adicionar ao final de `router.py`").

## 3. Onde cada regra de negócio entra

| RN | Arquivo · função | Como |
|---|---|---|
| RN05 | `<x>_usecase.py` · `open()` | `repository.find_by_id_for_update(...)` antes de decrementar |
| RN03 | `<mod>/handlers.py` + relay | evento `XExpired` + handler que devolve o estoque |
| RN01 | `<x>_usecase.py` · `open()` | contagem por CPF antes de confirmar |
| RN02 | `<aggregate>.py` · `refund_amount(now)` | cálculo puro no domínio |

## 4. DevOps (só se aplicável)

- Variáveis novas em `src/app/config.py` e `.env.example` (com
  `SECRET`/`SENSITIVE`/`CONFIG`).
- Segredo no CI (`gh secret set ... --repo gcarvalhow/api.ludens`) e `env:` no job
  `lint-and-test` do `.github/workflows/ci.yml`.

## 5. Passo a passo TBD (Backend)

```
git checkout master && git pull && git checkout -b feat/<NN>-<slug>
# commit 1 — domínio
git add src/app/modules/<mod>/domain && git commit -m "feat(<mod>): modelar <x> e eventos de domínio"
# commit 2 — application
git add src/app/modules/<mod>/application && git commit -m "feat(<mod>): usecase e schemas de <x>"
# commit 3 — infrastructure + outbox
git add src/app/modules/<mod>/infrastructure src/app/modules/<mod>/handlers.py src/app/outbox && git commit -m "feat(<mod>): repositório, serviço e handlers de <x>"
# commit 4 — api + migration
git add src/app/modules/<mod>/api src/app/modules/<mod>/router.py src/app/modules/<mod>/dependencies.py migrations && git commit -m "feat(<mod>): expor rotas de <x> e migration"
```
Depois: `/team-ludens:tbd-pr` (senior-dev Modo 2 + `/code-review`) → push → PR
`Closes #<NN>` → merge (1 aprovação + CI verde).

## 6. Ordem entre as superfícies

Backend e QA (casos de domínio) começam juntos a partir do `logic.md`. Frontend
começa em paralelo contra o contrato-alvo do `integration.md`. O `integration.md`
canônico e a integração real só depois do merge do backend.

## 7. Bloqueios em aberto

Liste `[bloqueio: decidir antes de implementar]` herdado de `spec.md`/`logic.md`.
Nenhuma fatia com bloqueio aberto vira issue.
