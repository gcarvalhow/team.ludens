---
name: frontend-architecture
description: Regras canônicas de arquitetura e código para o frontend (web.ludens) do Ludens — Next.js (App Router) + React + TypeScript estrito, feature-based, TanStack Query + Zod + react-hook-form + shadcn/ui + Tailwind. Carregar antes de qualquer implementação em web.ludens. Contém 14 arquivos de referência. Escopo é web.ludens — para o backend use backend-architecture.
---

# Frontend Architecture — Regras Canônicas de Código

Esta é a skill mestra de arquitetura e código do frontend do Ludens
(`web.ludens`) — a aplicação web onde o comprador descobre espetáculos, reserva
assentos, paga com Pix e acompanha as compras, e o admin do teatro gerencia
espetáculos e sessões.

**Ação obrigatória ao carregar esta skill:**

Ler TODOS os arquivos de referência em `skills/frontend-architecture/references/`
em ordem numérica. Não pular nenhum. Não resumir. Ler na íntegra.

---

## Stack

- **Next.js (App Router) + React** — SPA/SSR híbrido; rotas em `src/app/`.
- **TypeScript em modo estrito** (`strict`, `noImplicitAny`, `noUnusedLocals`,
  `exactOptionalPropertyTypes`, `moduleResolution: "bundler"`).
- **TanStack Query v5** — cache de servidor (queries + mutations).
- **Zod** — fonte de verdade do contrato de dados (parse de response, resolver de
  formulário). O tipo nasce do schema (`z.infer`), nunca uma `interface` manual.
- **react-hook-form** + `@hookform/resolvers/zod` — formulários.
- **shadcn/ui + Tailwind CSS** — design system.
- **Sonner** — toasts (sempre; nunca outra lib).
- **ESLint (config Next) + Prettier** — lint e formatação (portão de pipeline).
- UI em **pt-BR**, responsiva (mobile é pré-requisito do N2), **WCAG 2.1 AA** como
  referência.

> Mesma stack e mesmas regras de um frontend privado anterior do mesmo autor,
> adaptadas ao domínio do Ludens.

---

## Fonte de verdade viva

Esta skill descreve o padrão de código. Para contexto de produto e para o
contrato de cada feature, a fonte viva é `docs.ludens`:

- `docs.ludens/product/scope.md` e `problem.md` — contexto que fundamenta
  `references/00-project-context.md`.
- `docs.ludens/specs/[domínio]-[conceito]/integration.md` — o contrato
  backend→frontend de cada feature (rotas, request/response, erros).
- `docs.ludens/specs/[domínio]-[conceito]/logic.md` — estados e fluxos por perfil.

Se esta skill divergir do que `docs.ludens` ou o código real dizem, eles vencem —
pare e sinalize.

---

## Arquivos a carregar (ordem obrigatória)

```
00-project-context.md
01-architecture.md
02-creating-a-feature.md
03-typescript-and-schemas.md
04-queries.md
05-mutations.md
06-forms.md
07-components.md
08-naming-conventions.md
09-imports-and-barrels.md
10-build-and-quality.md
11-ux-principles.md
12-backend-boundary.md
13-testing.md
```

---

## Princípios de aplicação

### Toda regra é mandatória

Não são sugestões, não são guidelines opcionais. São regras. Obrigatórias.

### Em caso de conflito entre abordagens

Escolher a **mais restritiva**:
- `unknown` + narrowing com Zod ou um tipo genérico → `unknown` + Zod.
- Lógica no componente ou no hook → no hook.
- Barrel ou deep import → barrel.
- Recriar a query key inline ou usar `query-options.ts` → `query-options.ts`.
- Ajustar o componente pro shape errado da API ou transform na service → transform na service.
- `any` ou modelagem correta → modelagem correta.

### Violação detectada → parar e corrigir

1. Parar a task. 2. Identificar a regra (citar arquivo e seção). 3. Corrigir.
4. Continuar só após a correção. 5. Nunca avançar com violação conhecida.

---

## Resumo das regras mais críticas (referência rápida)

| Área | Regra mais crítica |
|------|--------------------|
| Tipos | `z.infer<typeof schema>` é a única fonte — nunca `interface` manual duplicando schema |
| Queries | `query-options.ts` é obrigatório — nunca recriar key ou fn fora dele |
| Mutations | Toda mutation invalida queries + toast de sucesso + toast de erro |
| Componentes | `components/ui/` nunca usa `useQuery`, `useMutation`, service, nem busca dado por id |
| Server/Client | Componente com hook/estado/handler leva `'use client'`; página/layout são Server Components por padrão |
| Imports | Barrel é entrega, não dívida — toda subpasta sai com `index.ts` |
| Build | `npm run build` (type check do Next) + `npm run lint` verdes antes de qualquer commit |
| Backend | Frontend nunca toca no repositório de backend — nunca |
| UX | Todo estado assíncrono trata loading + error + empty; contagem regressiva da reserva sempre visível (RN03) |
| Forms | O schema de **request** guia o form, nunca o de response |
| Git | Fluxo gerenciado por `/team-ludens:tbd-start`, `/team-ludens:tbd-commit`, `/team-ludens:tbd-pr` |
