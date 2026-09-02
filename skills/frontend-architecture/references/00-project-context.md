# Contexto do Projeto — `web.ludens`

O `web.ludens` é a aplicação web do Ludens — plataforma de venda de ingressos de
um teatro comunitário. É voltada ao público (o comprador não precisa instalar
nada), em pt-BR, responsiva e acessível.

## Dois públicos, uma aplicação

- **Comprador** — descobre espetáculos, vê disponibilidade em tempo real, reserva
  assentos (reserva temporária de 15 min), paga com Pix, recebe confirmação,
  acompanha o histórico de compras, pede cancelamento/reembolso.
- **Admin (teatro)** — CRUD de espetáculo (título, sinopse, imagem, categoria) e
  de sessão (data, hora, capacidade, tipos e preços de ingresso). Uma sessão com
  ingressos vendidos não é deletada, só cancelada (dispara reembolso).

## Conceitos centrais

- `Show` (espetáculo) — título, sinopse, imagem, categoria/gênero, datas de
  sessões futuras, faixa de preço.
- `Session` (sessão) — data, hora, local, capacidade, tipos de ingresso
  (inteira/meia) e preços, **quantidade disponível em tempo real**.
- `Reservation` (reserva) — bloqueio temporário de ingressos durante o checkout;
  expira em 15 min e devolve os ingressos (RN03).
- `Order` (pedido) — compra confirmada, ligada ao comprador; status
  confirmada/cancelada/reembolsada.
- `Ticket` (ingresso) — código único / QR, validável na entrada; tipo inteira ou
  meia.
- `Buyer` (comprador) — conta com CPF, e-mail, senha (identity).

## Stack alvo

- **Next.js (App Router) + React** · **TypeScript estrito**
- **TanStack Query v5** · **Zod** · **react-hook-form** + `@hookform/resolvers/zod`
- **shadcn/ui** + **Tailwind CSS** · **Sonner** (toasts)
- ESLint (config Next) + Prettier

O projeto é frontend-first no dia a dia. O backend (`api.ludens`) existe e é
separado — **nunca é tocado a partir deste repo** (`references/12`).

## Tema

Não há tema escuro forçado (isso era do produto interno da DOM Med). O Ludens é
público: contraste e legibilidade seguem **WCAG 2.1 AA**; se houver alternância
de tema, é escolha do usuário, não hardcode.

## Domínios da aplicação (features)

```
src/features/
  catalog     → vitrine, busca/filtro, detalhe da sessão, gestão (admin)
  booking     → seleção de quantidade/tipo, reserva temporária, contagem regressiva
  checkout    → pagamento Pix, tela de aguardando confirmação, confirmação
  account     → registro, login, recuperação de senha, histórico, cancelamento/reembolso
```

`booking` e `checkout` podem ser uma feature só se o fluxo for curto — decisão
registrada no `README.md` da feature.

## Rotas (App Router — `src/app/`)

| Rota | Feature | Acesso |
|---|---|---|
| `/login`, `/registro`, `/recuperar-senha`, `/redefinir-senha` | account | Público |
| `/` | catalog | Público |
| `/espetaculos/[showId]` | catalog | Público |
| `/sessoes/[sessionId]` | catalog | Público |
| `/checkout/[reservationId]` | checkout | Autenticado |
| `/pedido/[orderId]` | checkout | Autenticado (dono) |
| `/minhas-compras`, `/minhas-compras/[orderId]` | account | Autenticado |
| `/admin/espetaculos` | catalog (admin) | Admin |

Páginas e layouts são **Server Components** por padrão. Componentes com hooks,
estado ou handlers levam `'use client'`.

## Relação com a API de backend

O projeto consome **uma** API (`api.ludens`). O contrato de cada feature está em
`docs.ludens/specs/[domínio]-[conceito]/integration.md`. Acesso exclusivamente
via camada `server/services/` de cada feature, a partir do registro central em
`src/routes/endpoints.ts`.

Convenções globais ainda `<a definir>` no backend (ver o `integration.md`):
prefixo de rota / base path, versionamento de API, forma exata do corpo de erro.
Enquanto isso, o frontend trabalha contra o contrato-alvo e absorve o shape final
via transform na service layer.

## Usuário real

O comprador típico decide de última hora, no celular, sem paciência para
aprender. O caminho feliz (descoberta → confirmação) tem que caber em **≤ 5
passos** (RNF04). Toda ação assíncrona precisa de feedback claro de
sucesso/erro; a reserva sempre mostra **quanto tempo resta** antes de expirar.
