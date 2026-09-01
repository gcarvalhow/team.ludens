---
name: feature-implementation-spec
description: >
  Peça final do pipeline de spec do Ludens. A partir de uma spec + logic doc
  revisados, produz o mapa de TODO o código a implementar — por responsável
  (Backend / Frontend / QA / DevOps) — com os arquivos reais, o esqueleto de
  código a colar, e o passo a passo Trunk-Based Development de ponta a ponta.
  É o que cada issue referencia para a tropa "só colar e deixar na estrutura".
user-invocable: true
argument-hint: "[domínio]-[conceito] (ex: booking-reservation)"
---

# Feature Implementation Spec

A `spec.md` diz o que construir. O `logic.md` diz como o produto se comporta.
**Este documento diz exatamente qual código escrever, onde, em que ordem, e como
levar da branch ao merge sem erro.**

O objetivo é que cada membro do time abra a sua issue, encontre a fatia dele
(backend, frontend ou QA) já quebrada em arquivos e passos, cole o esqueleto na
estrutura do repo, e siga o passo a passo TBD até o PR — sem ter que redescobrir
a arquitetura nem adivinhar a sequência.

---

## Pré-condições (não negociáveis)

1. Existe `docs.ludens/specs/[domínio]-[conceito]/spec.md` com `status: approved`.
2. Existe `docs.ludens/specs/[domínio]-[conceito]/logic.md` com `status: reviewed`
   (revisado pelos tech leads de FE e BE).

Se qualquer uma faltar, **pare** e aponte a etapa que falta no pipeline
(`feature-design` → aprovação PO → `logic-design` → revisão FE+BE → aqui).

---

## Leitura obrigatória

- A `spec.md` e o `logic.md` da feature
- `docs.ludens/requirements/functional.md` (o RF) e `business-rules.md` (as RN)
- `docs.ludens/backend/overview.md` — anatomia de módulo, skeleton de arquivos,
  os 5 módulos (`identity`, `catalog`, `booking`, `payment`, `notification`)
- `docs.ludens/backend/integration/_template.md` — a estrutura do contrato
  backend→frontend

---

## Processo

### 1. Parecer de Backend

`Agent(subagent_type: team-ludens:senior-dev)` rodando com o contexto de
`api.ludens` (a skill `backend-architecture`). Peça, para esta feature:
- Módulo(s) afetado(s) e se é módulo novo ou extensão.
- Lista de arquivos a criar/alterar, **em ordem de dependência**:
  `domain/` (aggregates, entities, value_objects, enumerations, events) →
  `application/` (schemas request/response, usecases) →
  `infrastructure/` (repositories, services) →
  `api/routers/` + `router.py` + `dependencies.py` (se exportar algo) →
  `migrations/versions/` (Alembic).
- Eventos de domínio a emitir e handlers de outbox (in-process) a registrar.
- Onde as RN entram no código (RN05 → `find_by_id_for_update`; RN03 → relay de
  expiração; RN01 → validação no usecase; RN02 → cálculo no domínio).

### 2. Parecer de Frontend

`Agent(subagent_type: team-ludens:senior-dev)` com o contexto de `web.ludens`
(a skill `frontend-architecture`). Peça, para esta feature:
- Feature-pasta afetada e se é nova ou extensão.
- Arquivos a criar/alterar, **em ordem de dependência**:
  `routes/endpoints.js` → `schemas/` → `services/` →
  `hooks/queries/query-options.js` + `hooks/queries/` → `hooks/mutations/` →
  `hooks/forms/` → `components/` → `components/ui/` → barrels `index.js`.
- Contrato consumido (aponta o `integration.md` da feature, mesmo que ainda seja
  o contrato-alvo — ver seção "integration.md" abaixo).
- Estados assíncronos a tratar (loading / error / empty) e mensagens de erro em
  linguagem de negócio.

### 3. Parecer de QA

`Agent(subagent_type: team-ludens:qa-engineer)`: checagem de DoR, casos de teste
de domínio (pytest) a colar, roteiro de teste manual pré-entrega, riscos.

### 4. Montar o documento

Preencha `templates/implementation-spec.md` com os três pareceres, salve em
`docs.ludens/specs/[domínio]-[conceito]/implementation-spec.md`. Preencha também
o **contrato-alvo** em `templates/integration.md` → salve como
`docs.ludens/specs/[domínio]-[conceito]/integration.md` (marcado como
`status: alvo` — vira canônico só depois que o backend implementar; o backend
atualiza para refletir o código real ao fim).

### 5. Fatiar em issues

Ao final, oriente o usuário a rodar `/team-ludens:tbd-start` uma vez por fatia:
- **1 issue-mãe** por feature (`feat: [nome]`, `Issue Type = feature`), com a
  visão e o link para a pasta de spec.
- **1 sub-issue por responsável** (`Backend` / `Frontend` / `QA`), cada uma com a
  seção "Escopo" = a checklist de arquivos/passos daquela responsabilidade
  copiada deste documento, marcada como sub-issue da issue-mãe (`Parent issue`
  no Project). DevOps só ganha issue se a feature exigir variável/segredo/CI
  novo.
- Labels: `module: [domínio]` + `N1` (ou `N2`/`N3`).

---

## Regras de qualidade do documento

- **Todo arquivo listado tem caminho real** na anatomia do módulo/feature — nunca
  "crie um serviço para X". Se o senior-dev não soube dar o caminho exato, isso
  é uma lacuna a resolver antes de fatiar, não um detalhe a deixar em aberto.
- **Todo passo TBD é executável sem interpretação**: o comando de branch, a
  ordem dos commits (um por camada, mensagem Conventional Commits pt-BR
  sugerida), o corpo do PR, o gate de review.
- **Nada de regra de negócio implícita**: cada RN citada aparece com o arquivo e
  a função onde é aplicada.
- **O documento não inventa contrato**: se o `logic.md` deixou uma pergunta
  aberta, ela reaparece aqui como `[bloqueio: decidir antes de implementar]`, não
  como suposição.
