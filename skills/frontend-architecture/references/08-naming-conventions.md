# Convenções de Nomenclatura

Fonte cruzada: `docs.ludens/backend/code-style.md` (seção frontend).

## Código

- **Variáveis e funções:** `camelCase` (`fetchSessionById`, `reservationTimeLeft`).
- **Componentes e arquivos de componente:** `PascalCase` (`SessionDetail.jsx`,
  `CheckoutPage.jsx`).
- **Hooks:** `useXxx` (`useBookingMutations`, `useRegisterForm`).
- **Arquivos não-componente:** `kebab-case` ou `camelCase` conforme o padrão da
  pasta — schemas `{entity}.schema.js`, services `{entity}.service.js`,
  constants `{feature}.constants.js`.
- **Query keys builders:** `{entity}Keys` (`sessionKeys`, `orderKeys`).
- **Barrels:** sempre `index.js`.

## Domínio — vocabulário em inglês

Identificadores de domínio seguem os termos do backend, em inglês: `Show`,
`Session`, `Reservation`, `Order`, `Ticket`, `Buyer`, `full`/`half`.
**Comentários em português.** Texto visível ao usuário em **pt-BR**.

## Processo

- Nomes de branch em **inglês** (`feat/7-ticket-reservation`).
- Issues, user stories e mensagens de commit em **português**.
- Conventional Commits (`feat`, `fix`, `refactor`, `docs`, `test`, `chore`),
  mensagem imperativa em português, escopo = feature (`feat(booking): ...`).

## Rotas

Caminhos de rota em **português** (`/minhas-compras`, `/espetaculos/:showId`) —
são URL voltada ao usuário. Os `params` seguem `camelCase` (`showId`,
`sessionId`, `reservationId`).
