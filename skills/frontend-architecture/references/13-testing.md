# Testes — Jest + Playwright

Teste é parte do contrato de entrega, não apêndice.

- **Jest** sempre que houver mudança de lógica, contrato ou camada reutilizável.
- **Playwright** sempre que houver fluxo navegável, UI, formulário, feedback
  visual ou comportamento do usuário.
- Nunca encerrar com "não testado" sem explicação objetiva.

> `docs.ludens/backend/testing.md` registra que os testes de componente do
> frontend ainda são um alvo — o único portão automatizado hoje é `lint` + `build`.
> Esta referência descreve o padrão-alvo (mesmo de um frontend privado anterior); introduzir a
> suíte de fato é uma decisão a registrar em `docs.ludens` antes de virar gate.

## O que cada camada valida

### Jest

`schemas/` e transforms · `server/services/` e parsing · `hooks/queries/` ·
`hooks/mutations/` · `hooks/forms/` · `lib/` · `constants/` com semântica.

Isso inclui: parse de response, validação de campos, transforms, `enabled`
condicional, `invalidate`/`refetch`, rollback, submit logic, composição de payload.

### Playwright

Páginas (App Router) · dialogs/sheets/drawers · navegação · submits de formulário
· toasts · estados loading/empty/error · interações reais · fluxos do produto.

## Comandos

```bash
npm run test
npm run test:watch
npx playwright test
```

Não documentar comando que não existe no `package.json`.

## O que testar com Jest

- **Schemas:** parse válido/inválido, nulidade, opcionalidade, datas, `refine`.
- **Services:** URL certa, parse certo da response, shape final, `void`,
  propagação de erro, transform de shape (`references/12`).
- **Query hooks:** uso correto das `queryOptions`, `enabled`, `select`.
- **Mutation hooks:** `mutationFn` correta, `invalidate`/`refetch`, toast de
  sucesso e erro, rollback em UI otimista.
- **Form hooks:** default values, `reset` em edição, submit create/update,
  composição de payload.

## Fluxos Playwright do Ludens (checklist)

- vitrine carrega e filtra por data/gênero;
- abrir o detalhe da sessão, ver `availableCount` atualizar no polling;
- reservar → cair no checkout com o contador rodando;
- deixar a reserva expirar → mensagem de expiração, lugares voltam;
- pagar no sandbox do AbacatePay → "aguardando" → confirmação com ingressos;
- pagamento recusado → reserva liberada;
- login/registro e redirecionamento;
- "Minhas compras": ver pedido, reenviar ingresso, cancelar dentro da janela (RN02);
- admin: criar espetáculo + sessão, publicar, ver na vitrine; tentar excluir
  sessão vendida (recusado) → cancelar.

## Estrutura

```
src/features/{feature}/schemas/{entity}.schema.test.ts
src/features/{feature}/hooks/mutations/use{Entity}Mutations.test.ts
__tests__/e2e/{feature}/{fluxo}.spec.ts
```

O nome do spec explica o fluxo, não só a feature (`ticket-reservation.spec.ts`,
não `booking.spec.ts`).

## Como reportar

O que foi rodado, o que passou, o que falhou, se a falha é pré-existente ou nova,
e se algum teste não se aplicava.

## Anti-padrões

- inventar comando que não existe no repo;
- testar só manualmente e reportar como automação;
- não testar UI alterada;
- deixar mutation crítica sem teste nem validação de fluxo;
- esconder falha preexistente em frase genérica.
