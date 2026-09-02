# Convenções de Nomenclatura

Nomear bem é parte da arquitetura. O nome deve comunicar o papel do arquivo, a
camada, o domínio da feature, e se é UI, hook, service, type, schema ou doc.

## Pastas

Sempre `kebab-case`: `src/features/catalog/`, `src/features/account/hooks/queries/`.

## Arquivos por camada

| Camada | Convenção | Exemplo |
| --- | --- | --- |
| Schema | `{entity}.schema.ts` | `session.schema.ts` |
| Service | `{entity}.service.ts` | `reservation.service.ts` |
| Types | `{entity}.types.ts` | `order.types.ts` |
| Query hook | `use{Name}Queries.ts` | `useCatalogQueries.ts` |
| Mutation hook | `use{Name}Mutations.ts` | `useReservationMutations.ts` |
| Form hook | `use{Name}Form.ts` | `useRegisterForm.ts` |
| Component hook | `use{Name}.ts` | `useCheckoutFlow.ts` |
| Query options | `query-options.ts` | (nome fixo, com hífen) |
| Visual form | `{Name}Form.tsx` | `RegisterForm.tsx` |
| Componente | `{Name}.tsx` | `SessionDetail.tsx` |
| Constants | `{feature}.constants.ts` | `booking.constants.ts` |
| Barrel | `index.ts` | — |
| Rota | `page.tsx` / `layout.tsx` | (App Router) |

## Componentes React exportados

`PascalCase` (nome e arquivo): `SessionCard.tsx`, `TicketPicker.tsx`,
`OrderStatusBadge.tsx`.

## Features

Refletem o domínio real: `catalog`, `booking`, `checkout`, `account`. Evitar
siglas, nomes técnicos em vez de domínio, `utils-feature`, ou pastas
camelCase/PascalCase em `src/features`.

## Functions

- Services de leitura: prefixo `fetch` (`fetchShows`, `fetchSessionById`).
- Services de escrita: ação explícita (`openReservation`, `cancelOrder`,
  `createShow`, `updateSession`).
- Handlers locais: prefixo `handle` (`handleSubmit`, `handleCancel`).
- Helpers puros: nome pelo efeito, sem prefixo React (`formatPrice`,
  `buildReservationPayload`, `refundLabel`).

## Tipos

- Entidades: `PascalCase`, singular (`Session`, `Order`, `Buyer`).
- DTOs: `PascalCase` + sufixo `DTO` (`OpenReservationDTO`, `UpdateSessionDTO`).
- Props: `PascalCase` + `Props` (`SessionCardProps`).
- Context value: `PascalCase` + `ContextValue` (`AuthContextValue`).

## Query keys

Constante: `{entity}QueryKeys` (`sessionQueryKeys`, `orderQueryKeys`). Estrutura:
`all`, `lists`, `details`, `detail`, `filtered`.

## Constantes exportadas

`SCREAMING_SNAKE_CASE`: `RESERVATION_TTL_SECONDS`, `MAX_TICKETS_PER_CPF`,
`ORDER_STATUS_LABELS`, `POLLING_INTERVAL_MS`. Helper puro fica `camelCase`.

## Domínio — vocabulário em inglês

Identificadores de domínio seguem os termos do backend, em inglês: `Show`,
`Session`, `Reservation`, `Order`, `Ticket`, `Buyer`, `full`/`half`.
**Comentários em português.** Texto visível ao usuário em **pt-BR**.

## Rotas e URLs

Caminhos de rota em **português** (`/minhas-compras`, `/espetaculos/[showId]`) —
são URL voltada ao usuário. Segmentos dinâmicos em `camelCase`
(`[showId]`, `[sessionId]`, `[reservationId]`, `[orderId]`).

## Branches e commits

Fluxo git gerenciado por `/team-ludens:tbd-start` → `/team-ludens:tbd-commit` →
`/team-ludens:tbd-pr`. Branch base `master`. Branch em inglês
(`feat/7-ticket-reservation`); commits **Conventional Commits em português**, escopo
= feature: `feat(booking): adicionar contador de reserva`.

## O que evitar

- misturar kebab-case, camelCase e PascalCase sem critério;
- componente exportado com nome genérico demais;
- hook com nome que não diz se lê, escreve ou orquestra;
- DTO sem sufixo que o diferencie da entidade;
- `utils.ts` sem semântica;
- abreviações opacas em domínio de negócio.
