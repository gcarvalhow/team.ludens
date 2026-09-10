# Mapa de `docs.ludens` — Qual documento ler para qual assunto

`docs.ludens` é a documentação viva do produto e da engenharia, mantida contra o
código real. Esta referência mapeia qual arquivo ler dependendo do que você
precisa saber agora.

## Ponto de entrada

| Arquivo | Quando consultar |
|---|---|
| `backend/overview.md` | Visão geral do backend — os três padrões (DDD, monólito modular, Outbox in-process), os 5 módulos, o skeleton de arquivos de `api.ludens`, o fluxo end-to-end de compra. Comece por aqui sempre que a dúvida for "como isso funciona hoje". |

## ADRs — `backend/design/00x-*.md`

| ADR | Decide | Status |
|---|---|---|
| `001-outbox-in-process.md` | Por que efeitos colaterais (e-mail, estorno) viram linha `Event` na mesma transação, e um relay in-process (`asyncio.Task`, polling ~2s) chama handlers Python — **sem broker** | `proposto` (decidido, código a iniciar) |
| `002-monolito-modular.md` | Por que um único serviço deployável em módulos isolados; anatomia interna padrão de módulo; a lista dos 5 módulos | `proposto` |

## Requisitos

| Arquivo | Conteúdo |
|---|---|
| `requirements/functional.md` | RF01–RF09 — user story, critérios de aceite, dependências técnicas. Aprovados pelo PO em 2026-08-28. |
| `requirements/business-rules.md` | RN01 (6 ingressos/CPF/sessão), RN02 (reembolso por janela), RN03 (expiração 15 min), RN04 (meia sem documento), RN05 (disponibilidade atômica). |
| `requirements/overview.md` | RNF01–RNF06 — alvos numéricos (disponibilidade ≤ 1s p95; busca ≤ 2s p95; reserva ≤ 2s p95; e-mail ≤ 5 min; 99%/mês; ≤ 5 passos; WCAG 2.1 AA; Docker). Contam como critério de Definition of Ready. |

## Segurança

| Arquivo | Conteúdo |
|---|---|
| `backend/security/authentication.md` | Dual-token JWT HS256, `security_stamp`, bcrypt, cookie de refresh (`HttpOnly; Secure; SameSite=Strict`), roles `BUYER`/`ADMIN`. |
| `backend/security/configuration.md` | Toda variável de ambiente: tipo, valor padrão, classificação (`SECRET`/`SENSITIVE`/`CONFIG`). `JWT_SECRET_KEY`, `DATABASE_URL`, `ACCESS_TOKEN_EXPIRE_MINUTES` (30), `REFRESH_TOKEN_EXPIRE_DAYS` (7), `ALLOWED_ORIGINS`, `OUTBOX_RELAY_INTERVAL_SECONDS` (2). Features adicionam depois: chave/URL/webhook secret do AbacatePay; conexão SMTP + remetente; limite por CPF; TTL da reserva. |

## Contrato de integração

| Arquivo | Conteúdo |
|---|---|
| `backend/integration/_template.md` | Estrutura de 16 seções do contrato backend→frontend. Preenchido por feature em `specs/[domínio]-[conceito]/integration.md`. Convenções ainda `<preencher>`: prefixo de rota / base path, versionamento de API, forma exata do corpo de erro. |

## Specs de feature

| Arquivo | Conteúdo |
|---|---|
| `specs/[domínio]-[conceito]/spec.md` | O que a feature é e por quê (produto). |
| `specs/[domínio]-[conceito]/logic.md` | Regras, estados, contrato FE↔BE (negócio). |
| `specs/[domínio]-[conceito]/integration.md` | Contrato backend→frontend (rotas, request/response, erros). |
| `specs/[domínio]-[conceito]/backend.md` | Todo o código Python da feature, arquivo a arquivo, + passo a passo TBD. |
| `specs/[domínio]-[conceito]/frontend.md` | Todo o código `.ts`/`.tsx` da feature, arquivo a arquivo, + passo a passo TBD. |
| `specs/[domínio]-[conceito]/quality.md` | DoR, casos de domínio (pytest) com código, testes de integração, roteiro manual. |

## Time e processo

| Arquivo | Conteúdo |
|---|---|
| `team/maintainability.md` | Trunk-Based Development, Conventional Commits, feature flags, ~15% do ciclo para débito técnico. |
| `team/quality.md` | DoR / DoD. |
| `team/testing.md` / `backend/testing.md` | Estratégia de teste, gates de merge, script de QA manual. |
| `team/tech-debt.md` | Política de registro de débito técnico. |

## Regra de precedência

`docs.ludens` é mantida contra o código real — se esta skill e `docs.ludens`
divergirem, **`docs.ludens` e o código vencem**. Pare e sinalize a divergência em
vez de seguir uma regra desatualizada desta skill.
