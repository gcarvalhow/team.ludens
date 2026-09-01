# Queries (TanStack Query v5)

## `query-options.js` é obrigatório

Toda feature com leitura centraliza **query keys** e **query options** num único
`hooks/queries/query-options.js`. Nunca recriar uma key ou uma `queryFn` fora
dele.

```js
// catalog/hooks/queries/query-options.js
import { queryOptions } from '@tanstack/react-query';
import { fetchShows, fetchSessionById } from '@catalog/services';

export const showKeys = {
  all: ['shows'],
  list: (filters) => [...showKeys.all, 'list', filters ?? {}],
};
export const sessionKeys = {
  all: ['sessions'],
  detail: (id) => [...sessionKeys.all, 'detail', id],
};

export const catalogQueryOptions = {
  showList: (filters) => queryOptions({
    queryKey: showKeys.list(filters),
    queryFn: () => fetchShows(filters),
  }),
  sessionDetail: (id) => queryOptions({
    queryKey: sessionKeys.detail(id),
    queryFn: () => fetchSessionById(id),
    enabled: Boolean(id),
    staleTime: 5_000,           // RNF02: disponibilidade ≤ 1s p95 e muda rápido
    refetchInterval: 15_000,    // detalhe da sessão reflete disponibilidade quase-tempo-real
  }),
};
```

## Hooks de query

```js
// catalog/hooks/queries/useCatalogQueries.js
import { useQuery } from '@tanstack/react-query';
import { catalogQueryOptions } from './query-options';

export function useCatalogQueries() {
  return {
    useShowList: (filters) => useQuery(catalogQueryOptions.showList(filters)),
    useSessionDetail: (id) => useQuery(catalogQueryOptions.sessionDetail(id)),
  };
}
```

## Regras

- `hooks/queries/` **pode** usar `useQuery`, `useSuspenseQuery`,
  `useInfiniteQuery`, e reutilizar `query-options.js`.
- **Não pode** fazer mutation, chamar endpoint inline, ou fazer request fora de
  service.
- A key sempre vem de um builder no `query-options.js` — para que a invalidação
  em `hooks/mutations/` use exatamente a mesma key.
- `staleTime`/`refetchInterval` de disponibilidade (`sessionDetail`) são parte do
  contrato de produto (a pessoa não pode ver "10 lugares" e reservar num assento
  que já foi) — não mexer sem alinhar com o `logic.md` da feature.
