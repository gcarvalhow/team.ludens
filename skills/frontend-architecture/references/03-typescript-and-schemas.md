# TypeScript e Schemas

TypeScript e Zod sustentam o contrato de dados do frontend. O schema não é
acessório: é a fonte de verdade do formato da API e do payload que o frontend
envia.

Regra central:
- sempre que existir schema, o tipo nasce dele (`z.infer`);
- tipo manual só entra quando for composição legítima, não duplicação de contrato.

---

## Base técnica

TypeScript em modo estrito. O `tsconfig.json` liga, entre outras:

- `strict: true` · `noImplicitAny: true` · `noUnusedLocals: true`
- `exactOptionalPropertyTypes: true` · `moduleResolution: "bundler"`

Consequências reais:

- `any` implícito quebra o build;
- variável local não usada quebra o build;
- opcional e `undefined` não são a mesma coisa;
- imports precisam respeitar os aliases e a resolução moderna.

---

## Schema como fonte de verdade

### Response

```ts
import { z } from 'zod';

export const orderSchema = z.object({
  id: z.string().uuid(),
  status: z.enum(['pending', 'paid', 'refund_processing', 'refunded', 'failed']),
  amount: z.number(),
  createdAt: z.coerce.date(),
  tickets: z.array(z.object({
    id: z.string().uuid(),
    type: z.enum(['full', 'half']),
    code: z.string(),
  })),
  refundedAmount: z.number().nullable(),
});
```

### Request (DTO)

```ts
export const openReservationSchemaDTO = z.object({
  sessionId: z.string().uuid(),
  quantity: z.number().int().min(1, 'Escolha ao menos 1 ingresso').max(6),
  ticketType: z.enum(['full', 'half']),
});
```

### Tipos inferidos (em `server/types/`)

```ts
import type { z } from 'zod';
import type { orderSchema, openReservationSchemaDTO } from '@checkout/schemas';

export type Order = z.infer<typeof orderSchema>;
export type OpenReservationDTO = z.infer<typeof openReservationSchemaDTO>;
```

### O que evitar

```ts
// ❌ duplica contrato que já existe no schema
interface Order {
  id: string;
  status: string;
}
```

---

## DTO-first por entidade

Separar claramente: schema de entidade (response), schema de create DTO, schema
de update DTO, e schema de filtros/query params quando a feature exigir.

---

## Nulidade, optional e campo omitido

Frontend quebra integração quando trata `null`, `undefined` e ausência de campo
como iguais. Não são.

| Semântica | Schema certo |
| --- | --- |
| Campo sempre presente, pode ser `null` | `z.string().nullable()` |
| Campo pode não vir | `z.string().optional()` |
| Campo pode não vir ou ser `null` | `z.string().nullish()` |
| Campo sempre presente e nunca `null` | `z.string()` |

Regra: se o backend devolve `null` explícito → `.nullable()`; se **omite** a
propriedade → `.optional()`; se aceita ambos → `.nullish()`. Não usar `.optional()`
para "simular null". Se o `integration.md` da feature não deixa claro qual dos
dois, **pare e pergunte** (`references/12`).

---

## Datas

```ts
startsAt: z.coerce.date(),
refundedAt: z.coerce.date().nullable(),
```

Correto quando: a API devolve ISO string, o resto da feature opera com `Date`, e
a transformação é estável. Cuidado quando o campo pode vir vazio/`null`/formato
inconsistente, ou a feature só precisa exibir a string.

---

## Enums e valores fechados

`z.enum([...])` sempre que o contrato tiver um conjunto fechado. Só documente
como fechado o que o backend realmente estabilizou.

```ts
export const reservationStatusEnum = z.enum(['open', 'confirmed', 'expired', 'cancelled']);
```

---

## `exactOptionalPropertyTypes`

Não preencher objeto com `undefined` "só para completar". Omitir a chave quando o
contrato permite ausência:

```ts
const payload = {
  ticketType,
  ...(note ? { note } : {}),
};
```

## `noUnusedLocals`

Argumento ignorado: prefixar com `_`.

```ts
function handleError(_error: unknown) {
  toast.error('Erro inesperado.');
}
```

---

## Schemas aninhados

Construir do menor para o maior (reuso, legibilidade, testes isolados).

```ts
export const ticketSchema = z.object({
  id: z.string().uuid(),
  type: z.enum(['full', 'half']),
  code: z.string(),
  status: z.enum(['valid', 'invalid']),
});

export const orderSchema = z.object({
  id: z.string().uuid(),
  status: z.enum(['pending', 'paid', 'refund_processing', 'refunded', 'failed']),
  tickets: z.array(ticketSchema),
  createdAt: z.coerce.date(),
});
```

---

## `parse` vs `safeParse`

- **`parse`** — quando um contrato deveria ser válido e falha indica problema
  real. É o default da service layer: `return orderSchema.parse(data)`.
- **`safeParse`** — quando a invalidade é esperada/controlável (validação local
  exploratória de formulário).

---

## `server/types/` como API pública de tipos

Schema fica em `schemas/`; type público fica em `server/types/`. O resto da
feature importa de `server/types/`, não do schema cru:

```ts
import type { Order, OpenReservationDTO } from '@checkout/server/types';
```

---

## Resumo operacional

- schema é fonte de verdade; o tipo nasce dele (`z.infer`);
- `server/types/` é a superfície pública dos tipos;
- datas, nullabilidade e enums modelados com rigor;
- `exactOptionalPropertyTypes` exige omitir chave em vez de `undefined`;
- transformações em schema devem ser seguras e conscientes;
- `parse` na service; `safeParse` só em validação local.
