# Arquitetura do Frontend — `web.ludens`

Define o padrão ideal de arquitetura frontend. Não é um espelho literal de cada
arquivo existente — é o contrato para decisões novas e revisões.

Regra base: o frontend é **feature-based**, com fluxo de abstração previsível e
separação rígida entre infraestrutura, dados, orchestration e apresentação.

---

## Estrutura raiz

```
src/
  main.jsx                ← bootstrap (React Router + QueryClientProvider)
  App.jsx                 ← árvore de rotas
  routes/
    endpoints.js          ← registro centralizado de endpoints
  features/               ← features de domínio
  components/             ← componentes compartilhados verdadeiros (raro)
  hooks/                  ← hooks globais raros
  lib/                    ← utilitários e infra compartilhada (ex.: fetcher)
```

Regra operacional: procurar primeiro a feature dona do problema; só criar algo
global quando o código realmente não tem um único dono de feature.

## Estrutura ideal de uma feature

```
src/features/{feature}/
  schemas/
    {entity}.schema.js
    index.js
  services/
    {entity}.service.js
    index.js
  hooks/
    queries/
      query-options.js
      use{Entity}Queries.js
      index.js
    mutations/
      use{Entity}Mutations.js
      index.js
    forms/
      use{Entity}Form.js
      index.js
  components/
    ui/
      {Component}.jsx      ← apresentacional puro
      index.js
    {Component}.jsx        ← orchestration (conecta hooks + UI)
    index.js
  constants/
    {feature}.constants.js
    index.js
  lib/
    {helper}.js
    index.js
  README.md
  index.js                 ← API pública da feature
```

Nem toda feature precisa de todas as pastas. A que existir sai com `index.js`.

## Fluxo de abstração obrigatório

```
src/routes/endpoints.js
  ↓
schemas/            (contrato — Zod)
  ↓
services/           (chamada HTTP primitiva + parse + transform de shape)
  ↓
hooks/queries e hooks/mutations
  ↓
hooks/forms
  ↓
components/         (orchestration — conecta dados e UI)
  ↓
components/ui/      (apresentação pura — só props/callbacks)
```

Leitura prática: endpoints definem o endereço; schemas definem o contrato;
services fazem a chamada primitiva; hooks transformam em leitura/escrita
reutilizável; components conectam dados e UI; `components/ui` só renderiza.

### Violações proibidas

- `components/ui/` chamando `useQuery`, `useMutation` ou service;
- componente fazendo request direto;
- mutation vivendo dentro de um componente visual;
- service disparando toast;
- hook de query recriando endpoint inline em vez de usar service;
- lógica de negócio forte dentro de um componente de rota quando ela deveria
  viver na feature.

## Como decidir onde um código novo vive

1. **Identifique a feature dona.** Esse comportamento pertence a `catalog`,
   `booking`, `checkout`, `account`? É detalhe da feature ou realmente
   compartilhado?
2. **Descubra a camada certa.** Contrato de dados → `schemas/`. Request HTTP →
   `services/`. Leitura do servidor → `hooks/queries/`. Escrita → `hooks/mutations/`.
   Lógica de formulário → `hooks/forms/`. Orchestration de componente →
   `components/`. Visual puro → `components/ui/`.
3. **Verifique se já existe.** Procure schema, service, hook, `index.js`
   existentes. Estenda antes de abrir uma trilha paralela.

## Aliases

Configurar no `vite.config.js` (`resolve.alias`) e no `jsconfig.json`:

```
@/*            → src/*
@catalog/*     → src/features/catalog/*
@booking/*     → src/features/booking/*
@checkout/*    → src/features/checkout/*
@account/*     → src/features/account/*
```

Cruzou feature ou camada compartilhada → usar alias. Dentro da mesma feature →
usar a API pública por `index.js` quando houver. Import relativo longo
(`../../../features/...`) é sintoma de arquitetura ruim.

## O que esta arquitetura evita

Feature virando pasta de arquivos soltos; UI misturada com mutation e regra de
negócio; services fazendo papel de hook; deep imports espalhados; tipos/shapes
duplicados divergindo do schema; componentes de rota absorvendo responsabilidade
demais; código novo copiando padrões ruins de áreas legadas.
