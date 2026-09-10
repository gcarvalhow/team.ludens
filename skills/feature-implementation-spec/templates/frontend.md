# TEMPLATE — `frontend.md` (Ludens)

Todo o código de frontend de uma feature, arquivo a arquivo, pronto para colar.
Salvar como `docs.ludens/specs/[domínio]-[conceito]/frontend.md`.

> Pré-condição: `spec.md` (`approved`) e `logic.md` (`reviewed`) da mesma feature.
> Regra de ouro: **nenhum bloco de código com `...` ou `// TODO`** — conteúdo
> inteiro do arquivo, sempre.

---

## Frontmatter

```yaml
---
status: draft
spec: [domínio]-[conceito]
surface: frontend
created_at: AAAA-MM-DD
---
```

## Cabeçalho (igual nos três documentos)

```
# [Nome da feature] — Frontend
```

**Resumo:** 2–3 linhas do que a feature entrega, ponta a ponta.
**RF:** RFxx · **RN:** RNxx · **Feature frontend:** `account`
**Contrato:** `docs.ludens/specs/[domínio]-[conceito]/integration.md`
**Carregar antes:** skill `frontend-architecture` (todos os `references/`).

Stack: **Next.js (App Router) + TypeScript estrito**. Arquivos `.ts`/`.tsx`;
rotas em `src/app/**/page.tsx` (Server Components; `[id]` dinâmico, `await
params`); componentes/hooks com estado, handler ou hook de React levam
`'use client'`; tipo = `z.infer` do schema (nunca `interface` manual);
`query-options.ts` obrigatório; toda mutation invalida query + toast de sucesso +
toast de erro; `components/ui/` é apresentacional puro; barrel `index.ts` em toda
subpasta. Aliases: `@<feat>/*`, `@web/*`, `@components/*`.

---

## 1. Arquivos (ordem de dependência)

| # | Camada | Caminho | Novo/Editar |
|---|---|---|---|
| 1 | endpoints | `src/routes/endpoints.ts` | editar — adiciona o grupo da feature |
| 2 | schemas | `src/features/<feat>/schemas/<x>.schema.ts` | novo — Zod, response + DTO de request |
| 3 | server/types | `src/features/<feat>/server/types/index.ts` | novo — `z.infer` dos schemas |
| 4 | server/services | `src/features/<feat>/server/services/<x>.service.ts` | novo — request + `schema.parse`; transform de shape aqui |
| 5 | queries | `src/features/<feat>/hooks/queries/query-options.ts` | novo — keys hierárquicas + `queryOptions` |
| 6 | queries | `src/features/<feat>/hooks/queries/use<X>Queries.ts` | novo |
| 7 | mutations | `src/features/<feat>/hooks/mutations/use<X>Mutations.ts` | novo — invalida + toast |
| 8 | forms | `src/features/<feat>/hooks/forms/use<X>Form.ts` | novo — só se houver form; resolver = schema de request |
| 9 | components/ui | `src/features/<feat>/components/ui/<X>.tsx` | novo — apresentacional puro |
| 10 | components | `src/features/<feat>/components/<X>.tsx` | novo — `'use client'`; conecta hooks + UI; loading/error/empty |
| 11 | rota | `src/app/<caminho>/page.tsx` | novo — Server Component; prefetch + `HydrationBoundary` quando fizer sentido |
| 12 | barrels | `index.ts` em toda subpasta + raiz da feature | novo |
| 13 | README | `src/features/<feat>/README.md` | novo/editar |

## 2. Código

Para **cada** arquivo da tabela, um bloco assim (conteúdo inteiro):

```ts
// src/features/<feat>/schemas/<x>.schema.ts  — novo
import { z } from 'zod';
// ... arquivo completo, sem elipses ...
```

`endpoints.ts` já existe: mostrar o objeto do grupo novo inteiro e dizer onde
encaixa em `API_ENDPOINTS`.

## 3. Contrato consumido

Aponta `docs.ludens/specs/[domínio]-[conceito]/integration.md`. Enquanto o backend
não implementou, o frontend trabalha contra o **contrato-alvo**. Se ao integrar o
shape divergir, o ajuste é um transform na `server/services/` + registro da
divergência — nunca editar o repo de backend.

## 4. Estados assíncronos e mensagens

| Estado | Onde | Mensagem (linguagem de negócio) |
|---|---|---|
| loading | `<X>.tsx` | skeleton / spinner |
| error | `<X>.tsx` | ex.: "Não foi possível carregar a sessão. Tente de novo." |
| empty | `<X>.tsx` | ex.: "Você ainda não fez nenhuma compra." |

## 5. Passo a passo TBD (Frontend)

```
git checkout master && git pull && git checkout -b feat/<NN>-<slug>
# commit 1 — contrato
git add src/routes/endpoints.ts src/features/<feat>/schemas src/features/<feat>/server && git commit -m "feat(<feat>): endpoints, schemas, tipos e services de <x>"
# commit 2 — hooks
git add src/features/<feat>/hooks && git commit -m "feat(<feat>): queries, mutations e forms de <x>"
# commit 3 — UI + rota
git add src/features/<feat>/components src/app && git commit -m "feat(<feat>): telas, componentes e rota de <x>"
# commit 4 — barrels + README
git add src/features/<feat> && git commit -m "chore(<feat>): barrels index.ts e README da feature"
```
Depois: `npm run lint && npm run build` verdes → `/team-ludens:tbd-pr`.

## 6. Ordem entre as superfícies

Frontend pode começar contra o contrato-alvo do `integration.md` antes do backend.
A integração real é após o merge do backend.

## 7. Bloqueios em aberto

Liste `[bloqueio: decidir antes de implementar]` herdado de `spec.md`/`logic.md`.
