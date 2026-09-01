---
name: frontend-architecture
description: Regras canônicas de arquitetura e código para o frontend (web.ludens) do Ludens — React + Vite + JS/JSX, feature-based, TanStack Query + Zod + react-hook-form. Carregar antes de qualquer implementação em web.ludens. Contém 13 arquivos de referência. Escopo é web.ludens — para o backend use backend-architecture.
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

- **React 19 + Vite** — SPA, JavaScript/JSX (não TypeScript, não Next.js).
- **React Router** — roteamento client-side.
- **TanStack Query v5** — cache de servidor (queries + mutations).
- **Zod** — validação de contrato em runtime (funciona em JS; usada para
  `parse()` de response e resolver de formulário).
- **react-hook-form** — formulários.
- **ESLint + Prettier** — lint e formatação (obrigatório no pipeline:
  `npm run lint`).
- Toasts: uma lib de toast (`sonner` ou equivalente) padronizada no projeto.
- UI em **pt-BR**, responsiva (mobile é pré-requisito do N2), **WCAG 2.1 AA** como
  referência.

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
03-schemas-and-validation.md
04-queries.md
05-mutations.md
06-forms.md
07-components.md
08-naming-conventions.md
09-imports-and-barrels.md
10-build-and-quality.md
11-ux-principles.md
12-backend-boundary.md
```

---

## Princípios de aplicação

### Toda regra é mandatória

Não são sugestões, não são guidelines opcionais. São regras. Obrigatórias.

### Em caso de conflito entre abordagens

Escolher a **mais restritiva**:
- Colocar lógica no componente ou no hook → no hook.
- Barrel ou deep import → barrel.
- Recriar a query key inline ou usar `query-options.js` → `query-options.js`.
- Ajustar o componente pro shape errado da API ou fazer transform na service →
  transform na service.

### Violação detectada → parar e corrigir

1. Parar a task. 2. Identificar a regra (citar arquivo e seção). 3. Corrigir.
4. Continuar só após a correção. 5. Nunca avançar com violação conhecida.

---

## Resumo das regras mais críticas (referência rápida)

| Área | Regra mais crítica |
|------|--------------------|
| Contrato | `schemas/` (Zod) é a fonte do formato — nenhum shape duplicado à mão em outro lugar |
| Queries | `query-options.js` é obrigatório — nunca recriar key ou fn fora dele |
| Mutations | Toda mutation invalida queries + toast de sucesso + toast de erro |
| Componentes | `components/ui/` nunca usa `useQuery`, `useMutation` ou service |
| Imports | Barrel é entrega, não dívida — toda subpasta sai com `index.js` |
| Build | `npm run lint` e `npm run build` verdes antes de qualquer commit |
| Backend | Frontend nunca toca no repositório de backend — nunca |
| UX | Todo estado assíncrono trata loading + error + empty; contagem regressiva da reserva sempre visível (RN03) |
| Forms | O schema de request guia o form, nunca o schema de response |
| Git | Fluxo gerenciado por `/team-ludens:tbd-start`, `/team-ludens:tbd-commit`, `/team-ludens:tbd-pr` |
