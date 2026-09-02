# Como Criar uma Feature do Zero — `web.ludens`

O processo é **de baixo para cima**: começa pelo contrato, termina na interface.
Evita duas falhas comuns: criar interface sem contrato de dados claro; criar
camadas fora de ordem e depois tentar "encaixar".

## Quando criar uma feature nova

Só quando o domínio tem identidade própria no produto, fluxo e responsabilidades
próprios, e não é extensão natural de uma feature existente. `catalog`,
`booking`, `checkout`, `account` são legítimas. Um dialog a mais em `catalog`,
uma mutation extra em `account`, um utilitário de uma feature existente — não.

## Sequência obrigatória

### 1. Registrar endpoints em `src/routes/endpoints.ts`

```ts
const api = process.env.NEXT_PUBLIC_API_URL;
const withBase = (path = '') => `${api}${path}`;

export const API_ENDPOINTS = {
  catalog: {
    shows: {
      list: withBase('/shows'),
      byId: (id: string) => withBase(`/shows/${id}`),
    },
    sessions: {
      byId: (id: string) => withBase(`/sessions/${id}`),
    },
  },
};
```

Rotas parametrizadas são funções. Não hardcodar endpoint dentro de service.

### 2. Criar schemas em `schemas/` (Zod)

```ts
import { z } from 'zod';

export const sessionSchema = z.object({
  id: z.string().uuid(),
  showId: z.string().uuid(),
  startsAt: z.coerce.date(),
  capacity: z.number().int(),
  availableCount: z.number().int(),
  status: z.enum(['on_sale', 'sold_out', 'closed', 'cancelled']),
  ticketTypes: z.array(z.object({ type: z.enum(['full', 'half']), price: z.number() })),
});

export const openReservationSchemaDTO = z.object({
  sessionId: z.string().uuid(),
  quantity: z.number().int().min(1).max(6),
  ticketType: z.enum(['full', 'half']),
});
```

Um arquivo por entidade/DTO relevante. Response schema ≠ request schema. Modelar
`null`/`optional`/datas com rigor (`references/03`).

### 3. Expor tipos em `server/types/`

```ts
import type { z } from 'zod';
import type { sessionSchema, openReservationSchemaDTO } from '@catalog/schemas';

export type Session = z.infer<typeof sessionSchema>;
export type OpenReservationDTO = z.infer<typeof openReservationSchemaDTO>;
```

Preferir `type` inferido, nunca `interface` duplicando o schema.

### 4. Criar `server/services/`

```ts
import { fetcher } from '@web/lib/fetcher';
import { API_ENDPOINTS } from '@web/routes/endpoints';
import { sessionSchema } from '@catalog/schemas';

export async function fetchSessionById(id: string) {
  const { data } = await fetcher.get(API_ENDPOINTS.catalog.sessions.byId(id));
  return sessionSchema.parse(data);
}
```

Service faz request e `parse`, só isso. Sem toast, sem cache, sem hook de React.
Se o shape da API divergir do esperado, o **transform fica aqui** (`references/12`).

### 5. `hooks/queries/query-options.ts` (obrigatório)

Ver `references/04` — query keys hierárquicas + `queryOptions` centralizados.

### 6–8. Hooks de query, mutation, form

`references/04`, `05`, `06`.

### 9. Componentes

Ordem: `components/ui/` (visual puro) → `components/` (orchestration que conecta
hooks e UI, trata loading/error/empty). `references/07`.

### 10. Rota em `src/app/`

Criar a `page.tsx` (Server Component; `await params`); prefetch + `HydrationBoundary`
quando a tela se beneficia de dados já hidratados (`references/04`).

### 11. Barrels `index.ts` em TODA subpasta criada + na raiz da feature

Obrigatório, não opcional (`references/09`).

### 12. README da feature

`src/features/{feature}/README.md` — domínio, fluxo de dados, decisões relevantes
(ex.: por que `booking` e `checkout` são uma feature só, ou separadas).

## Ordem resumida

```
1. endpoints
2. schemas (Zod)
3. server/types (z.infer)
4. server/services
5. hooks/queries/query-options.ts
6. hooks/queries
7. hooks/mutations
8. hooks/forms (se houver form)
9. components/ui e components
10. rota em src/app/ (Server Component + prefetch quando fizer sentido)
11. barrels index.ts (todas as subpastas + feature raiz)
12. README
```

## Erros mais comuns

- Começar pelo componente e só depois descobrir o contrato de dados.
- Criar request inline no componente.
- Pular `query-options.ts`.
- Usar schema como tipo público em tudo sem organizar `server/types/`.
- Criar feature nova para algo que já pertence a uma existente.
- Inventar endpoint local em vez de registrar em `src/routes/endpoints.ts`.
- Criar arquivos das camadas sem criar os barrels — barrel não é dívida técnica,
  é parte da entrega.
- Concentrar regra de domínio num `page.tsx` em vez de na feature.
