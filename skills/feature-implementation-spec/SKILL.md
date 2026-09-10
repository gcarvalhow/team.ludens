---
name: feature-implementation-spec
description: >
  Peça final do pipeline de spec do Ludens. A partir de uma spec + logic doc
  revisados, produz TRÊS documentos de implementação por feature — backend.md,
  frontend.md e quality.md — cada um listando todo arquivo a criar/editar com o
  caminho real e o CÓDIGO COMPLETO pronto para colar, mais o passo a passo
  Trunk-Based Development. Não é mapa nem esqueleto: é o código.
user-invocable: true
argument-hint: "[domínio]-[conceito] (ex: booking-reservation)"
---

# Feature Implementation Spec

A `spec.md` diz o que construir. O `logic.md` diz como o produto se comporta.
**Estes três documentos dizem exatamente qual código escrever, em qual arquivo, e
como levar da branch ao merge.**

O objetivo é que cada pessoa do time abra o documento da sua superfície
(`backend.md`, `frontend.md` ou `quality.md`), e para cada arquivo listado
encontre o **conteúdo completo pronto para colar** — não uma descrição, não um
esqueleto com `...`, não uma assinatura sem corpo. Cola o arquivo no caminho
indicado, ajusta o que a realidade do repo pedir, e segue o passo a passo TBD até
o PR.

---

## Saída: três documentos, não um

Substitui o antigo `implementation-spec.md` único. Por feature, em
`docs.ludens/specs/[domínio]-[conceito]/`:

| Arquivo | Dono | Conteúdo |
| --- | --- | --- |
| `backend.md` | Backend | Todo arquivo Python a criar/editar em `api.ludens`, com código completo. Ordem `domain/ → application/ → infrastructure/ → outbox → api/ → migration`. Inclui a subseção **DevOps** (variáveis de ambiente, segredo de CI) quando a feature exigir. |
| `frontend.md` | Frontend | Todo arquivo `.ts`/`.tsx` a criar/editar em `web.ludens`, com código completo. Ordem `endpoints → schemas → server/types → server/services → hooks/queries → hooks/mutations → hooks/forms → components/ui → components → rota (src/app/) → barrels`. |
| `quality.md` | QA | Checagem de Definition of Ready; casos de teste de domínio (pytest) com o código completo; testes de integração cross-surface; roteiro de teste manual pré-entrega; riscos. |

Os três compartilham o mesmo cabeçalho (resumo, RF/RN, módulo, link do contrato)
e a mesma seção final **"Ordem entre as superfícies"** e **"Bloqueios em aberto"**.

O `integration.md` continua a ser gerado aqui como **contrato-alvo**
(`status: alvo`) e vira canônico quando o backend implementa.

---

## Pré-condições (não negociáveis)

1. Existe `docs.ludens/specs/[domínio]-[conceito]/spec.md` com `status: approved`.
2. Existe `docs.ludens/specs/[domínio]-[conceito]/logic.md` com `status: reviewed`.

Se qualquer uma faltar, **pare** e aponte a etapa que falta no pipeline
(`feature-design` → aprovação PO → `logic-design` → revisão FE+BE → aqui).

---

## Leitura obrigatória

- A `spec.md` e o `logic.md` da feature
- `docs.ludens/requirements/functional.md` (o RF) e `business-rules.md` (as RN)
- `docs.ludens/backend/overview.md` — anatomia de módulo, skeleton de arquivos,
  os 5 módulos (`identity`, `catalog`, `booking`, `payment`, `notification`)
- `docs.ludens/backend/integration/_template.md` — estrutura do contrato
- A skill `backend-architecture` **inteira** (todos os `references/`) antes de
  escrever qualquer código de `backend.md`
- A skill `frontend-architecture` **inteira** (todos os `references/`) antes de
  escrever qualquer código de `frontend.md`

---

## Processo

### 1. Parecer de Backend → `backend.md`

`Agent(subagent_type: team-ludens:senior-dev)` com o contexto de `api.ludens`.
Peça, para esta feature:

- Módulo(s) afetado(s) e se é módulo novo ou extensão.
- **A lista completa de arquivos** a criar/alterar em ordem de dependência:
  `domain/` (aggregates, entities, value_objects, enumerations, events) →
  `application/` (schemas request/response, usecases) →
  `infrastructure/` (repositories, services) →
  outbox (handler + registro no `outbox/registry.py`) →
  `api/routers/` + `router.py` + `dependencies.py` →
  `migrations/versions/` (Alembic).
- **Para cada arquivo, o conteúdo completo** seguindo `backend-architecture`
  (aggregate muda estado só via `raise_event`→`_when_*`; usecase orquestra numa
  transação; schema é contrato; nada de `except` vazio; funções ≤ ~30 linhas).
- Eventos de domínio emitidos e handlers de outbox registrados.
- Onde cada RN entra: arquivo + função (RN05 → `find_by_id_for_update`;
  RN03 → relay de expiração; RN01 → validação no usecase; RN02 → cálculo no
  domínio).
- Variáveis de ambiente novas (classificação `SECRET`/`SENSITIVE`/`CONFIG`) e o
  que muda no `ci.yml` — vira a subseção **DevOps** de `backend.md`.

### 2. Parecer de Frontend → `frontend.md`

`Agent(subagent_type: team-ludens:senior-dev)` com o contexto de `web.ludens`.
Peça, para esta feature:

- Feature-pasta afetada (`catalog` · `booking` · `checkout` · `account`) e se é
  nova ou extensão.
- **A lista completa de arquivos** em ordem de dependência:
  `src/routes/endpoints.ts` → `schemas/` → `server/types/` → `server/services/` →
  `hooks/queries/query-options.ts` + `hooks/queries/` → `hooks/mutations/` →
  `hooks/forms/` → `components/ui/` → `components/` → rota em `src/app/**/page.tsx`
  → barrels `index.ts` → `README.md` da feature.
- **Para cada arquivo, o conteúdo completo** seguindo `frontend-architecture`
  (TypeScript estrito; tipo = `z.infer` do schema, nunca `interface` manual;
  `query-options.ts` obrigatório; toda mutation invalida + toast de sucesso +
  toast de erro; `components/ui/` nunca fala com service; `'use client'` só onde
  há hook/estado/handler; `page.tsx` é Server Component).
- Contrato consumido: aponta o `integration.md` da feature (contrato-alvo
  enquanto o backend não implementou).
- Estados assíncronos tratados (loading / error / empty) e mensagens de erro em
  linguagem de negócio.

### 3. Parecer de QA → `quality.md`

`Agent(subagent_type: team-ludens:qa-engineer)`:

- Checagem item a item da Definition of Ready (`docs.ludens/team/quality.md`).
- **Casos de teste de domínio (pytest) com o código completo**, um arquivo de
  teste por aggregate/regra, salvável em `tests/modules/<mod>/`.
- Testes de integração cross-surface (o fluxo que atravessa backend + frontend)
  e o que cada um verifica.
- Roteiro de teste manual pré-entrega (fluxo principal + casos obrigatórios de
  RN + resiliência + restart).
- Riscos e pontos de atenção.

### 4. Montar os documentos

Preencha `templates/backend.md`, `templates/frontend.md` e `templates/quality.md`
com os pareceres e salve os três em
`docs.ludens/specs/[domínio]-[conceito]/`. Preencha também o contrato-alvo
(`templates/integration.md` → `integration.md`, `status: alvo`).

### 5. Fatiar em issues

Oriente o usuário a rodar `/team-ludens:tbd-start` uma vez por fatia:

- **1 issue-mãe** por feature (`Issue Type = feature`) em `docs.ludens`, com a
  visão e o link para a pasta de spec.
- **1 sub-issue por superfície** — `Backend` e `QA` em `api.ludens`, `Frontend`
  em `web.ludens` (`Issue Type = task`), cada uma com a seção "Escopo" = a
  checklist de arquivos daquele documento (`backend.md` / `frontend.md` /
  `quality.md`), ligada à issue-mãe por Sub-issue nativa (cross-repo funciona via
  `POST repos/<owner>/docs.ludens/issues/<n>/sub_issues` com
  `-F sub_issue_id=<databaseId>`).
- Campos no Project `@ludens`: `Status = Backlog`, `Priority`, `Area`
  (`backend`/`frontend`), `Issue Type`. Labels: `module: [domínio]` + `N1`
  (ou `N2`/`N3`).

---

## Regras de qualidade dos documentos

- **Código completo, não esqueleto.** Todo arquivo listado aparece num bloco de
  código com o caminho no comentário da primeira linha, marcado `# novo` ou
  `# editar`, e com o **conteúdo inteiro** — imports, classe/funções, corpo real,
  tratamento de erro. Num arquivo que já existe e só recebe um trecho, mostre a
  função/bloco novo inteiro com contexto suficiente para colar sem ambiguidade.
  Um bloco com `...` ou `# TODO: implementar` é falha do documento.
- **Todo caminho é real** na anatomia do módulo/feature — nunca "crie um serviço
  para X". Sem caminho exato = lacuna a resolver antes de fatiar.
- **Todo passo TBD é executável sem interpretação**: comando de branch, ordem dos
  commits (um por camada, Conventional Commits pt-BR), corpo do PR, gate de
  review.
- **Nada de regra de negócio implícita**: cada RN citada aparece com o arquivo e
  a função onde é aplicada.
- **Não inventa contrato**: pergunta aberta no `logic.md` reaparece como
  `[bloqueio: decidir antes de implementar]`, nunca como suposição.
- **Os três documentos fecham entre si**: o shape que o `frontend.md` faz
  `parse` com Zod é o mesmo que o `response.py` do `backend.md` devolve e o mesmo
  que o `integration.md` descreve. Divergência entre eles = falha do documento.
