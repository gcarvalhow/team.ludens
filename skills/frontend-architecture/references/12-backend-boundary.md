# Fronteira Frontend / Backend

O engenheiro de frontend é responsável por `web.ludens` e nada mais. O backend
(`api.ludens`) existe e é separado.

## Regra fundamental

**O frontend nunca edita arquivos no repositório de backend.** Sem exceções. Não
importa o motivo, a urgência ou a simplicidade da mudança.

## Quando o contrato de API está errado ou ausente

### Shape diferente do esperado

Não ajustar componente/hook/schema para "encaixar" o dado incorreto. **Fazer:**
um transform na **service layer** que converte o shape atual para o esperado, e
registrar a divergência.

```js
// converte snake_case da API para camelCase que o frontend usa
export async function fetchOrders() {
  const { data } = await fetcher.get(API_ENDPOINTS.account.orders.list);
  const raw = z.array(rawOrderSchema).parse(data);
  return raw.map((o) => ({ ...o, refundedAmount: o.refunded_amount }));
}
```

O transform fica **na service**, nunca no componente, hook ou schema.

### Endpoint ainda não existe

Não codificar a regra de negócio no frontend para compensar. **Fazer:** trabalhar
contra o **contrato-alvo** do `docs.ludens/specs/[domínio]-[conceito]/integration.md`
(gerado pela skill `feature-implementation-spec`), com um mock local claramente
marcado `// TODO: remover quando <rota> existir`. Quando o backend entregar,
remover o mock **sem alterar nenhum outro arquivo** — se precisar mexer em
schema/service/hook, o contrato não foi acordado antes.

### Contrato ambíguo

Não assumir o comportamento. **Fazer:** parar, registrar a ambiguidade no
`integration.md` da feature (seção "Lacunas e decisões em aberto") e perguntar ao
responsável de backend. Exemplo: "o campo `refundedAmount` vem `null` ou ausente
quando não há reembolso? — afeta `.nullable()` vs `.optional()` no schema".

## Onde as regras de negócio vivem

**Backend:** consistência de disponibilidade (RN05), limite por CPF (RN01),
política de reembolso (RN02), expiração de reserva (RN03), transições de estado de
ordem, autorização (o que cada perfil pode fazer). O frontend **consome o
resultado da API** — não duplica a regra. Se a API não devolve o que a UI precisa
para decidir, isso é uma lacuna de contrato a registrar, não uma regra a
reimplementar.

**Frontend:** validação de forma no formulário (formato, presença, faixa),
ordenação visual de listas, estado de UI local (drawer, aba, filtro temporário),
formatação para exibição (datas, rótulos de status, máscara de CPF), loading /
error / empty.

## Dados sensíveis

Nunca `localStorage` direto para CPF, e-mail, histórico ou qualquer dado pessoal
(RNF01). Usar o padrão de auth da feature `account`. `localStorage` só para
preferência de UI não sensível, documentada no código.

## Comunicação de dependência de backend

Quando uma feature depende de rota ainda não entregue: registrar no
`integration.md` da feature, e na descrição do PR uma seção "Dependências de
backend" listando o pendente. Não abrir o PR como se estivesse completo quando há
dependência bloqueante.
