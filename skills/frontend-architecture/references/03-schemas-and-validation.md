# Schemas e Validação (Zod em JS)

O `web.ludens` é JavaScript, não TypeScript — mas **Zod continua sendo a fonte do
contrato**. Zod valida em runtime; não depende de TypeScript.

## Regras

- **Um schema por entidade/DTO relevante**, em `schemas/{entity}.schema.js`.
- **Response schema ≠ request schema.** O schema de response modela o que a API
  devolve; os de create/update modelam o payload enviado. Nunca reusar um pelo
  outro.
- **Modelar `null`/`optional`/datas com precisão.** `z.coerce.date()` para
  timestamps ISO; `.nullable()` quando o campo vem `null`; `.optional()` quando
  pode vir ausente. Se o `integration.md` da feature não deixa claro qual dos
  dois, **pare e pergunte** — não assuma (ver `references/12`).
- **`parse()` sempre na service layer**, no retorno da chamada. Uma resposta que
  não bate o schema é um erro de contrato — deixe estourar, não silencie.
- **Nada de shape duplicado à mão.** Se você precisa de um "tipo" para
  documentar, exporte um JSDoc `@typedef` derivado do schema, não uma segunda
  descrição do formato.

## Exemplo

```js
// account/schemas/order.schema.js
import { z } from 'zod';

export const orderSchema = z.object({
  id: z.string().uuid(),
  status: z.enum(['confirmed', 'cancelled', 'refunded']),
  total: z.number(),
  createdAt: z.coerce.date(),
  tickets: z.array(z.object({
    id: z.string().uuid(),
    type: z.enum(['full', 'half']),
    code: z.string(),          // id único / QR (RF05)
  })),
  refundedAmount: z.number().nullable(),
});

export const requestRefundSchema = z.object({
  orderId: z.string().uuid(),
  reason: z.string().min(1, 'Descreva o motivo').max(500),
});

/** @typedef {z.infer<typeof orderSchema>} Order */  // só para documentação
```

## Validação de formulário

O resolver de `react-hook-form` usa o **schema de request** (`requestRefundSchema`
acima), nunca o de response. Ver `references/06`.

## O que não pode

- Fazer request num schema.
- Importar hook ou componente num schema.
- Esconder regra de negócio extensa num `.refine()` que deveria estar
  documentada no `logic.md` da feature — validação de forma (formato de CPF,
  quantidade entre 1 e 6) é ok; "sessão esgotada" é estado de servidor, não vem
  pro schema.
