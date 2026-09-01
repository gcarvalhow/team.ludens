# Contexto do Projeto — `web.ludens`

O `web.ludens` é a aplicação web do Ludens — plataforma de venda de ingressos de
um teatro comunitário. Dois públicos, uma aplicação:

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
- `Order` (ordem) — compra confirmada, ligada ao comprador; status
  confirmada/cancelada/reembolsada.
- `Ticket` (ingresso) — id único / QR, validável na entrada; tipo inteira ou
  meia.

## Domínios da aplicação (features)

```
catalog    → busca e filtro de espetáculos, detalhe da sessão, gestão (admin)
booking    → seleção de quantidade/tipo, reserva temporária, contagem regressiva
checkout   → pagamento Pix, tela de aguardando confirmação, confirmação
account    → registro, login, recuperação de senha, histórico, cancelamento/reembolso
```

(As pastas exatas de feature seguem `references/01`. `booking`/`checkout` podem
ser uma feature só se o fluxo for curto — decisão de arquitetura registrada no
README da feature.)

## Rotas (React Router)

| Rota | Feature | Acesso |
|---|---|---|
| `/login`, `/registro`, `/recuperar-senha` | account | Público |
| `/` | catalog | Público |
| `/espetaculos/:showId` | catalog | Público |
| `/sessoes/:sessionId` | catalog | Público |
| `/checkout/:reservationId` | checkout | Autenticado |
| `/minhas-compras` | account | Autenticado |
| `/admin/espetaculos` | catalog (admin) | Admin |

## Relação com a API de backend

O projeto consome **uma** API (`api.ludens`). O contrato de cada feature está em
`docs.ludens/specs/[domínio]-[conceito]/integration.md`. Acesso exclusivamente
via camada `services/` de cada feature, a partir do registro central em
`src/routes/endpoints.js`.

Convenções globais ainda `<a definir>` no backend (ver o `integration.md`):
prefixo de rota / base path, versionamento de API, forma exata do corpo de erro.
Enquanto isso, o frontend trabalha contra o contrato-alvo e absorve o shape final
via transform na service layer.

## Usuário real

O comprador típico decide de última hora, no celular, sem paciência para
aprender. O caminho feliz (descoberta → confirmação) tem que caber em **≤ 5
passos** (RNF04). Toda ação assíncrona precisa de feedback claro de
sucesso/erro; a reserva sempre mostra **quanto tempo resta** antes de expirar.
