# Contexto do Projeto — `api.ludens`

## Negócio

O Ludens é a plataforma de venda de ingressos de um teatro comunitário. Hoje a
venda acontece em dois canais desconectados (bilheteria física e vendas
informais pela internet) e **não há fonte única de disponibilidade de assentos
por sessão** — o mesmo assento chega a ser vendido duas vezes. O `api.ludens` é o
backend que se torna essa fonte única: expõe a API REST, valida entrada,
persiste estado, controla disponibilidade de forma atômica e dispara efeitos
(e-mail de confirmação, estorno) via outbox.

Critério de sucesso central: **duas compras concorrentes nunca podem, juntas,
exceder a capacidade da sessão** (RN05), mesmo sob acesso simultâneo.

## Split de repositórios

- **`api.ludens`** (este) — API FastAPI, monólito modular + DDD.
- **`web.ludens`** — frontend React + Vite. Nunca é tocado a partir deste repo.
- **`docs.ludens`** — produto, requisitos, arquitetura, specs. Fonte de entrada.

Não há repositório de worker — o Ludens não executa automações. Os efeitos
colaterais (e-mail, estorno) rodam como handlers Python no mesmo processo da API
(`references/07`).

## Stack real

- **Python 3.12 · FastAPI** — framework HTTP.
- **PostgreSQL** via **SQLAlchemy async** — fonte de verdade de todo o domínio
  (`buyers`, `refresh_tokens`, `shows`, `sessions`, `reservations`, `orders`,
  `tickets`, `events`).
- **Alembic** — migrations, em `migrations/versions/`.
- **`pydantic-settings`** — toda config lida de `.env.local` (dev) ou
  `.env.production` (prod), via `src/app/config.py`. A aplicação **falha na
  inicialização** se faltar uma variável obrigatória.
- **Ruff** — lint, obrigatório no pipeline (`ruff check .`).
- **Pytest** — testes (`pytest -q`), obrigatório no pipeline.
- **Docker / Docker Compose** — runtime padrão local e de pipeline. A API sobe
  via container, não `uvicorn` no host.
- **Sem Redis. Sem RabbitMQ / broker. Sem Event Sourcing. Sem CQRS.**

## Autenticação

Dual-token JWT HS256 (detalhe completo em
`docs.ludens/backend/security/authentication.md`):

- **Access token** curto (`Authorization: Bearer`, padrão 30 min; claims `sub`,
  `role`, `security_stamp`, `type`, `exp`, `iat`).
- **Refresh token** opaco (hash SHA-256 comparado contra o DB, padrão 7 dias,
  cookie `HttpOnly; Secure; SameSite=Strict` com `Path` restrito).
- **`security_stamp`** (UUID) regenerado no logout e na troca/recuperação de
  senha — invalida todos os tokens anteriores.
- Senhas: **bcrypt**. Roles: binário `BUYER | ADMIN` (sem permissão granular).
- O módulo `identity` exporta `get_current_buyer` e `require_admin`.

## Módulos existentes

Cinco módulos sob `src/app/modules/` (`docs.ludens/backend/design/002-monolito-modular.md`):

```
identity/     → registro e autenticação do comprador; histórico de compras (RF06, RF09)
catalog/      → espetáculos e sessões; disponibilidade em tempo real (RF01, RF02, RF08)
booking/      → reserva temporária, controle de estoque, emissão de ingresso (RF03, RF05 · RN01, RN03, RN05)
payment/      → cobrança Pix (AbacatePay) e ordens (RF04, RF07 · RN02)
notification/ → e-mails transacionais (handlers de evento; sem aggregate próprio) (RF05, RF09)
```

## Infra de desenvolvimento

```bash
docker compose -f docker/docker-compose.Development.yml up -d   # sobe PostgreSQL
alembic upgrade head
python scripts/seed_admin.py
```

API em `:8000`, OpenAPI em `/docs`. Hostnames em `.env.local` apontam para nomes
de container, nunca `localhost`.

## Fonte primária de verdade sobre o estado atual

O `CLAUDE.md` na raiz de `api.ludens` cobre terminologia e o estado corrente do
código. Este documento e as referências descrevem o padrão e o porquê. Para o
estado vivo — o que está implementado, contrato exato de cada rota, schema real
do banco — a fonte é `docs.ludens/backend/*` e as specs em `docs.ludens/specs/`.
Ver `references/10`.
