# Arquitetura do Frontend — `web.ludens`

Define o padrão ideal de arquitetura frontend. Não é um espelho literal de cada
arquivo — é o contrato para decisões novas e revisões.

Regra base: o frontend é **feature-based**, com fluxo de abstração previsível e
separação rígida entre infraestrutura, dados, orchestration e apresentação. O
App Router do Next.js dita a estrutura de **entrada** (rotas), não a arquitetura
das features.

---

## Estrutura raiz

```
src/
  app/                    ← rotas, layouts e páginas (App Router) — Server Components por padrão
    layout.tsx
    page.tsx
    (rotas...)/page.tsx
    providers.tsx         ← QueryClientProvider, Toaster ('use client')
  features/               ← features de domínio (catalog, booking, checkout, account)
  components/             ← componentes compartilhados verdadeiros (raro)
  components/ui/          ← shadcn/ui (design system)
  hooks/                  ← hooks globais raros
  lib/                    ← utilitários e infra compartilhada (ex.: fetcher)
  routes/
    endpoints.ts          ← registro centralizado de endpoints
  types/                  ← tipos globais raros
```

Regra operacional: procurar primeiro a feature dona do problema; só criar algo
global quando o código realmente não tem um único dono de feature.
`src/app/` é entrypoint de rota, **não** o lugar para concentrar regra de negócio
de feature.

## Estrutura ideal de uma feature

```
src/features/{feature}/
  schemas/
    {entity}.schema.ts
    index.ts
  server/
    services/
      {entity}.service.ts
      index.ts
    types/
      {entity}.types.ts       ← API pública de tipos (z.infer dos schemas)
      index.ts
    index.ts
  hooks/
    queries/
      query-options.ts
      use{Entity}Queries.ts
      index.ts
    mutations/
      use{Entity}Mutations.ts
      index.ts
    forms/
      use{Entity}Form.ts
      index.ts
    components/
      use{Component}.ts        ← orchestration de componente que cresceu
      index.ts
    index.ts
  contexts/
    index.ts
  constants/
    {feature}.constants.ts
    index.ts
  lib/
    {helper}.ts
    index.ts
  components/
    forms/
      {Entity}Form.tsx
      index.ts
    ui/
      {Component}.tsx          ← apresentacional puro da feature
      index.ts
    {Component}.tsx            ← orchestration (conecta hooks + UI)
    index.ts
  README.md
  index.ts                     ← API pública da feature
```

Nem toda feature precisa de todas as pastas. A que existir sai com `index.ts`.
`server/types/` é a superfície pública de tipos — não exportar tipo direto dos
schemas pela árvore toda.

## Fluxo de abstração obrigatório

```
src/routes/endpoints.ts
  ↓
schemas/            (contrato — Zod)
  ↓
server/services/    (chamada HTTP primitiva + parse + transform de shape)
  ↓
server/types/       (z.infer — API pública de tipos)
  ↓
hooks/queries e hooks/mutations
  ↓
hooks/forms e hooks/components
  ↓
components/         (orchestration — conecta dados e UI)
  ↓
components/ui/      (apresentação pura — só props/callbacks)
```

Leitura prática: endpoints definem o endereço; schemas definem o contrato;
services fazem a chamada primitiva; hooks transformam em leitura/escrita
reutilizável; components conectam dados e UI; `components/ui` só renderiza.

### Violações proibidas

- `components/ui/` chamando `useQuery`, `useMutation`, service ou `fetcher`;
- componente fazendo request direto;
- mutation vivendo dentro de um componente visual;
- service disparando toast;
- hook de query recriando endpoint inline em vez de usar service;
- lógica de negócio forte dentro de um `page.tsx` quando ela deveria viver na feature.

## App Router — Server vs Client Components

- `page.tsx`, `layout.tsx` e componentes sem interatividade são **Server
  Components** por padrão. Podem buscar dados direto quando fizer sentido, e
  fazer **prefetch + hidratação** das mesmas `queryOptions` (`references/04`).
- Componente com `useState`/`useEffect`/hooks de query/mutation/handlers levam
  `'use client'` no topo do arquivo.
- `params` é assíncrono no App Router moderno:

```tsx
export default async function Page({ params }: { params: Promise<{ sessionId: string }> }) {
  const { sessionId } = await params;
  return <SessionDetail sessionId={sessionId} />;
}
```

- A lógica de domínio fica na feature, não espalhada nas páginas.

## Como decidir onde um código novo vive

1. **Identifique a feature dona.** Pertence a `catalog`, `booking`, `checkout`,
   `account`? É detalhe da feature ou realmente compartilhado?
2. **Descubra a camada certa.** Contrato de dados → `schemas/`. Request HTTP →
   `server/services/`. Tipo público → `server/types/`. Leitura do servidor →
   `hooks/queries/`. Escrita → `hooks/mutations/`. Lógica de formulário →
   `hooks/forms/`. Orchestration de componente → `hooks/components/` ou
   `components/`. Visual puro → `components/ui/`.
3. **Verifique se já existe.** Procure schema, service, hook, `index.ts`
   existentes. Estenda antes de abrir uma trilha paralela.

## Aliases

Configurar em `tsconfig.json` (`compilerOptions.paths`) — e o Next resolve
sozinho:

```
@web/*        → src/*
@components/* → src/components/*
@catalog/*    → src/features/catalog/*
@booking/*    → src/features/booking/*
@checkout/*   → src/features/checkout/*
@account/*    → src/features/account/*
```

Cruzou feature ou camada compartilhada → usar alias. Dentro da mesma feature →
usar a API pública por `index.ts` quando houver. Import relativo longo
(`../../../features/...`) é sintoma de arquitetura ruim (`references/09`).

## O que esta arquitetura evita

Feature virando pasta de arquivos soltos; UI misturada com mutation e regra de
negócio; services fazendo papel de hook; deep imports espalhados; tipos
duplicados divergindo do schema; páginas absorvendo responsabilidade demais;
código novo copiando padrões ruins de áreas legadas.
