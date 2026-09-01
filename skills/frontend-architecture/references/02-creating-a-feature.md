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

### 1. Registrar endpoints em `src/routes/endpoints.js`

```js
const api = import.meta.env.VITE_API_URL;
const withBase = (path = '') => `${api}${path}`;

export const API_ENDPOINTS = {
  catalog: {
    shows: {
      list: withBase('/shows'),
      byId: (id) => withBase(`/shows/${id}`),
    },
    sessions: {
      byId: (id) => withBase(`/sessions/${id}`),
    },
  },
};
```

Rotas parametrizadas são funções. Não hardcodar endpoint dentro de service.

### 2. Criar schemas em `schemas/` (Zod)

```js
import { z } from 'zod';

export const sessionSchema = z.object({
  id: z.string().uuid(),
  showId: z.string().uuid(),
  startsAt: z.coerce.date(),
  capacity: z.number().int(),
  availableCount: z.number().int(),
  ticketTypes: z.array(z.object({
    type: z.enum(['full', 'half']),
    price: z.number(),
  })),
  isOnSale: z.boolean(),
});

export const openReservationSchema = z.object({
  sessionId: z.string().uuid(),
  quantity: z.number().int().min(1).max(6),
  ticketType: z.enum(['full', 'half']),
});
```

Um arquivo por entidade ou DTO relevante. Distinguir response schema de
create/update. Modelar `null`/`optional`/datas com precisão. **Não duplicar o
shape numa estrutura à mão em outro lugar** — o schema é a fonte.

### 3. Criar `services/`

```js
import { fetcher } from '@/lib/fetcher';
import { API_ENDPOINTS } from '@/routes/endpoints';
import { sessionSchema } from '@catalog/schemas';

export async function fetchSessionById(id) {
  const { data } = await fetcher.get(API_ENDPOINTS.catalog.sessions.byId(id));
  return sessionSchema.parse(data);
}
```

Service faz request e `parse`, só isso. Sem toast, sem cache, sem hook de React.
Se o shape da API divergir do esperado, o **transform fica aqui** (não no
componente, não no hook, não no schema) — ver `references/12`.

### 4. `hooks/queries/query-options.js` (obrigatório)

```js
import { queryOptions } from '@tanstack/react-query';
import { fetchSessionById } from '@catalog/services';

export const sessionKeys = {
  all: ['sessions'],
  detail: (id) => [...sessionKeys.all, 'detail', id],
};

export const sessionQueryOptions = {
  detail: (id) => queryOptions({
    queryKey: sessionKeys.detail(id),
    queryFn: () => fetchSessionById(id),
    enabled: Boolean(id),
    // disponibilidade muda rápido — refetch curto na tela de detalhe da sessão
    staleTime: 5_000,
  }),
};
```

### 5–7. Hooks de query, mutation, form

Ver `references/04`, `05`, `06`.

### 8. Componentes

Ordem: `components/ui/` (visual puro) → `components/` (orchestration que conecta
hooks e UI, trata loading/error/empty).

### 9. Barrels `index.js` em TODA subpasta criada + na raiz da feature

Obrigatório, não opcional. Ver `references/09`.

### 10. README da feature

`src/features/{feature}/README.md` — domínio, fluxo de dados, decisões relevantes
(ex.: por que `booking` e `checkout` são uma feature só, ou separadas).

## Ordem resumida

```
1. endpoints
2. schemas (Zod)
3. services
4. hooks/queries/query-options.js
5. hooks/queries
6. hooks/mutations
7. hooks/forms (se houver form)
8. components/ui e components
9. barrels index.js (todas as subpastas + feature raiz)
10. README
```

## Erros mais comuns

- Começar pelo componente e só depois descobrir o contrato de dados.
- Criar request inline no componente.
- Pular `query-options.js`.
- Criar feature nova para algo que já pertence a uma existente.
- Inventar endpoint local em vez de registrar em `src/routes/endpoints.js`.
- Criar arquivos das camadas sem criar os barrels — barrel não é dívida técnica,
  é parte da entrega.
