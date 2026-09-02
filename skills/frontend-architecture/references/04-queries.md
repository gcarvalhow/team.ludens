# Queries — TanStack Query v5

Queries são a camada oficial de leitura do servidor. Toda leitura que venha de
uma service da feature é encapsulada em hooks de query, com `query-options.ts`
como centro de definição de chave, função e política de cache.

- service faz request;
- `query-options.ts` define o contrato da query;
- hook expõe isso para o componente;
- componente consome o hook, **nunca** a service.

---

## `query-options.ts` é obrigatório

Toda feature com queries tem `hooks/queries/query-options.ts`. Centraliza query
keys, query options e `enabled`/`staleTime`/`select`/`refetchInterval` quando
fizer sentido.

```ts
import { queryOptions } from '@tanstack/react-query';
import { fetchShows, fetchSessionById } from '@catalog/server/services';
import type { ShowFiltersDTO } from '@catalog/server/types';

export const showQueryKeys = {
  all: ['shows'] as const,
  lists: () => [...showQueryKeys.all, 'list'] as const,
  filtered: (filters: ShowFiltersDTO) => [...showQueryKeys.lists(), filters] as const,
};

export const sessionQueryKeys = {
  all: ['sessions'] as const,
  details: () => [...sessionQueryKeys.all, 'detail'] as const,
  detail: (id: string) => [...sessionQueryKeys.details(), id] as const,
};

export const catalogQueryOptions = {
  showList: (filters: ShowFiltersDTO) =>
    queryOptions({
      queryKey: showQueryKeys.filtered(filters),
      queryFn: () => fetchShows(filters),
    }),
  sessionDetail: (id: string) =>
    queryOptions({
      queryKey: sessionQueryKeys.detail(id),
      queryFn: () => fetchSessionById(id),
      enabled: Boolean(id),
      // disponibilidade muda rápido — RNF02 (≤ 1 s p95) e RN05
      staleTime: 5_000,
      refetchInterval: 15_000,
    }),
};
```

Sem esse arquivo: query keys duplicadas/divergentes, invalidações imprecisas,
query functions recriadas em vários lugares, refactor difícil.

---

## Convenção de query keys

Hierárquica e previsível: `all` (família), `lists` (coleções), `details`
(namespace de detalhe), `detail(id)` (instância), `filtered(filters)` quando há
filtro. O objeto de key precisa ser estável, sem duplicação acidental. Filtro que
muda o resultado **entra na key**.

---

## Hooks de query — finos

Não recriam `queryKey` nem `queryFn`.

```ts
import { useQuery } from '@tanstack/react-query';
import { catalogQueryOptions } from './query-options';
import type { ShowFiltersDTO } from '@catalog/server/types';

export function useCatalogQueries() {
  return {
    useShowList: (filters: ShowFiltersDTO) => useQuery(catalogQueryOptions.showList(filters)),
    useSessionDetail: (id: string) => useQuery(catalogQueryOptions.sessionDetail(id)),
  };
}
```

---

## `enabled`

Query dependente de parâmetro opcional documenta e centraliza `enabled` no
`query-options.ts` — o componente não esconde isso em branches paralelas.

---

## Prefetch e hidratação (Server Components)

Quando uma rota entrega UI já hidratada com dados, prefetch com as **mesmas**
`queryOptions` — nunca uma versão paralela só para SSR.

```tsx
import { dehydrate, HydrationBoundary, QueryClient } from '@tanstack/react-query';
import { catalogQueryOptions } from '@catalog/hooks/queries';

export default async function Page() {
  const queryClient = new QueryClient();
  await queryClient.prefetchQuery(catalogQueryOptions.showList({}));
  return (
    <HydrationBoundary state={dehydrate(queryClient)}>
      <ShowGrid />
    </HydrationBoundary>
  );
}
```

---

## `staleTime` e polling

Não existe `staleTime` universal — reflete o domínio.

- **Dados estáveis** (catálogo de gêneros, detalhe de espetáculo): `staleTime` maior.
- **Dados operacionais** (`availableCount` da sessão, status de pedido `pending`,
  reserva `open`): `staleTime` curto + `refetchInterval` explícito. A pessoa não
  pode ver "10 lugares" e reservar num assento que já foi. Não mexer nesses
  valores sem alinhar com o `logic.md` da feature.

---

## `select`, `placeholderData`, `initialData`

- `select` transforma dado de leitura no cache.
- `placeholderData` melhora continuidade visual entre filtros (sem "piscada").
- `initialData` é para bootstrap legítimo, não para esconder ausência de fetch.

---

## O que NÃO pode ficar inline

`queryKey` reescrita à mão; `queryFn` recriada; endpoint manual; parsing da
response fora da service; regra de invalidar/refetch dentro do componente.

## Anti-padrões

- chamar service direto em componente;
- string literal de query key fora de `query-options.ts`;
- key sem hierarquia por conveniência;
- filtro escondido em closure sem refletir na key;
- usar a query como mutation disfarçada;
- hook de query com toast de regra de negócio.
