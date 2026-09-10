# Onde procurar em docs.ludens

| Assunto | Arquivo(s) |
|---|---|
| Problema, critérios de sucesso, visão | `product/problem.md` |
| Escopo (dentro/fora), níveis N1/N2/N3, premissas | `product/scope.md` |
| Requisitos funcionais (RF01–RF09) — user story, critérios, dependências | `requirements/functional.md` |
| Regras de negócio (RN01–RN05) | `requirements/business-rules.md` |
| Requisitos não-funcionais (RNF01–RNF06) — alvos numéricos | `requirements/overview.md` |
| Decisão/arquitetura técnica de backend | `backend/design/*.md` (ADRs: 001 outbox in-process, 002 monólito modular) |
| Visão geral do backend, anatomia de módulo, skeleton de arquivos | `backend/overview.md` |
| Contrato de integração backend→frontend (por feature) | `backend/integration/_template.md` e, por feature, `specs/[domínio]-[conceito]/integration.md` |
| Autenticação, tokens, security_stamp, roles | `backend/security/authentication.md` |
| Variáveis de ambiente, classificação de segredo | `backend/security/configuration.md` |
| Estilo de código (Python/React), convenções de idioma | `backend/code-style.md` |
| Estratégia de teste, gates de merge, script de QA manual | `backend/testing.md` |
| Papéis do time, RACI, ownership de documentação | `team/overview.md` |
| Setup local de dev, fluxo de branch | `team/development.md` |
| Trunk-Based Development, Conventional Commits, feature flags | `team/maintainability.md` |
| DoR / DoD | `team/quality.md` |
| Política de débito técnico, orçamento de ciclo (~15%) | `team/tech-debt.md` |
| Spec de uma feature específica (o que + regras + contrato + código) | `specs/[domínio]-[conceito]/{spec,logic,integration,backend,frontend,quality}.md` |

`docs.ludens` é mantida contra o código real — se um doc e o código divergirem, o
código vence. Sinalize a divergência em vez de seguir uma regra desatualizada.
