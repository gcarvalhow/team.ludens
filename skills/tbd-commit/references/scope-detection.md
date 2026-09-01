# Como detectar escopo (Conventional Commits)

A estrutura muda de repo para repo (backend monólito modular, frontend
feature-based, docs) — nunca hardcode uma lista fixa de escopos.

- **Backend (`api.ludens`):** primeiro diretório de módulo tocado dentro de
  `src/app/modules/` (`identity`, `catalog`, `booking`, `payment`,
  `notification`) ou `core` / `outbox` se a mudança é na base.
- **Frontend (`web.ludens`):** feature de domínio tocada (`catalog`, `booking`,
  `checkout`, `account`, `admin`) ou área transversal (`components`, `lib`,
  `routes`).
- **Infra/config em qualquer repo** (`docker/`, `Dockerfile`, `pyproject.toml`,
  `package.json`, `.github/`, `migrations/`): usa esse nome (`docker`, `deps`,
  `ci`, `migrations`).
- **`docs.ludens`:** `specs`, `backend`, `requirements`, `team`, `product` —
  a pasta tocada.
- Cruza áreas **sem relação lógica entre si** (motivos diferentes, não uma mesma
  mudança que naturalmente toca vários lugares): pare, explique o que
  identificou, pergunte se separa em commits (`git restore --staged` no segundo
  assunto) ou confirma um único commit mesmo assim.
- Mudança ampla mas de um mesmo assunto, ou sem escopo claro: omita o escopo.

Exemplos válidos:

```
feat(booking): adicionar reserva temporária com expiração de 15 minutos
fix(booking): impedir reserva concorrente de exceder a capacidade da sessão
feat(payment): integrar cobrança pix via abacatepay
feat(catalog): listar espetáculos com filtro por data e gênero
chore(docker): fixar postgres 16 no compose de desenvolvimento
docs(specs): adicionar spec e logic de booking-reservation
test(booking): cobrir expiração de reserva devolvendo ingressos
```
