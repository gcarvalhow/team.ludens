# Ludens Team — Plugin Claude Code

Marketplace/plugin Claude Code (`team-ludens`) com os papéis de time, o
pipeline de spec e o fluxo de desenvolvimento compartilhados entre os
repositórios do Ludens (`api.ludens`, `web.ludens`, `docs.ludens`). Não é um
repositório de produto — é a ferramentaria que os outros repos consomem.

A documentação de produto, requisitos e arquitetura vive em
[`docs.ludens`](https://github.com/gcarvalhow/docs.ludens). As **specs de
feature** (o que a tropa implementa) ficam em `docs.ludens/specs/[domínio]-[conceito]/`.

## Estrutura

```
team.ludens/
├── .claude-plugin/
│   ├── marketplace.json    # 3 plugins granulares (core / backend / frontend)
│   └── plugin.json         # metadata compartilhada (nome, versão, autor)
├── agents/
│   ├── product-thinking.md # cérebro de produto — dispara feature-design, protege coerência
│   ├── senior-dev.md       # spec de implementação + revisão de conformidade (só leitura)
│   └── qa-engineer.md      # DoR/DoD, roteiro de teste manual, casos de teste de domínio
├── skills/
│   ├── tbd-start/          # fluxo TBD — iniciar task (issue + branch + link no Project)
│   ├── tbd-commit/         # fluxo TBD — commit Conventional Commits
│   ├── tbd-pr/             # fluxo TBD — abrir PR / finalizar ciclo
│   ├── tbd-scope/          # fluxo TBD — Tech Lead, escopar antes de abrir issue
│   ├── setup/              # checa git/gh/python
│   ├── feature-design/     # pipeline de spec — mentalidade Steve Jobs → spec.md
│   ├── logic-design/       # pipeline de spec — regras/estados/contrato FE↔BE → logic.md
│   ├── feature-implementation-spec/ # pipeline de spec — código completo por superfície + passo a passo TBD → backend.md / frontend.md / quality.md
│   ├── backend-architecture/  # arquitetura de código do api.ludens
│   └── frontend-architecture/ # arquitetura de código do web.ludens
└── scripts/
    ├── guard_mutations.py  # hook PreToolUse — bloqueia mutação via Bash pros agents consultivos
    └── setup_reminder.py   # hook SessionStart (entrada core) — avisa se /team-ludens:setup ainda não rodou neste repo
```

## Instalação granular por repo

Cada repo consumidor habilita só o(s) plugin(s) que precisa — não instala tudo.

| Plugin | Conteúdo | Quem habilita |
|---|---|---|
| `core` | pipeline de spec (`feature-design` → `logic-design` → `feature-implementation-spec`) + fluxo `tbd-*` + `setup` + agents `product-thinking`/`senior-dev`/`qa-engineer` | todo repo |
| `backend` | skill `backend-architecture` | `api.ludens` |
| `frontend` | skill `frontend-architecture` | `web.ludens` |

Cada repo declara isso no próprio `.claude/settings.json`
(`extraKnownMarketplaces` + `enabledPlugins`) — commitado, não é configuração
pessoal.

### Passo a passo

1. Adicione o snippet ao `.claude/settings.json` do repo consumidor (commitado),
   ajustando `enabledPlugins` conforme a tabela — ex.: `web.ludens` habilita
   `core` + `frontend`.

   ```json
   {
     "extraKnownMarketplaces": {
       "team-ludens": {
         "source": { "source": "github", "repo": "gcarvalhow/team.ludens" }
       }
     },
     "enabledPlugins": {
       "core@team-ludens": true,
       "frontend@team-ludens": true
     }
   }
   ```

2. Depois do prompt de trust do Claude Code, instale de fato — `claude plugin
   install` aceita **um plugin por comando**:

   ```powershell
   claude plugin marketplace add gcarvalhow/team.ludens
   claude plugin install core@team-ludens --scope project
   claude plugin install frontend@team-ludens --scope project
   ```

   Confirme com `claude plugin list` que todos aparecem como `enabled`.

3. **Abra uma sessão nova** do Claude Code nesse repo — plugins instalados no
   meio de uma sessão em andamento não carregam skills/agents automaticamente.

4. Rode `/team-ludens:setup` — valida git/gh/python e aponta o que corrigir.

## Como uma mudança aqui chega nos repos consumidores

**Não é automático.** Mergear em `master` aqui não propaga sozinho — cada repo
consumidor precisa atualizar explicitamente e abrir uma sessão nova.

```powershell
claude plugin marketplace update team-ludens
claude plugin update core@team-ludens --scope project
```

**Gotcha crítico:** `claude plugin update` decide se há atualização comparando o
campo `version` de `.claude-plugin/plugin.json` — **não** o commit. Toda mudança
aqui que precise chegar aos consumidores exige, antes ou logo depois do merge:

```powershell
# em .claude-plugin/plugin.json, bump version (semver: patch pra fix, minor pra feat)
claude plugin tag --push
```

## O pipeline completo

```
/team-ludens:feature-design    (mentalidade Steve Jobs → docs.ludens/specs/[domínio]-[conceito]/spec.md)
        ↓ aprovação humana (PO)
/team-ludens:logic-design      (regras/estados/contrato FE↔BE → logic.md)
        ↓ revisão conjunta FE + BE tech lead
/team-ludens:feature-implementation-spec   (código completo por superfície + passo a passo TBD → backend.md / frontend.md / quality.md)
        ↓
/team-ludens:tbd-scope   (opcional, Tech Lead — grounding no estado real antes de abrir issue)
        ↓
/team-ludens:tbd-start   (issue-mãe + sub-issues por responsável + branch, linkadas no Project @ludens)
        ↓
implementação, carregando a skill de arquitetura do repo (backend/frontend-architecture)
        ↓
senior-dev (Modo 2, conformidade) + /code-review (nativa, bugs/qualidade) — recomendado, não bloqueante
        ↓
/team-ludens:tbd-commit  (quantos forem necessários — Conventional Commits pt-BR)
        ↓
/team-ludens:tbd-pr      (abre PR; rodado de novo após merge, finaliza o ciclo)
```

## Convenções (de `docs.ludens`)

- **Trunk-Based Development** — `master` é o único branch longevo; branches curtas
  `feature/nome` ou `fix/descricao` (inglês), reintegradas em poucos dias via PR
  pequeno; 1 aprovação + pipeline verde (lint + testes + Docker build) pra merge.
- **Conventional Commits** em português imperativo (`feat`, `fix`, `refactor`,
  `docs`, `test`, `chore`).
- **Idioma** — issues, user stories e commits em português; nomes de branch,
  identificadores de código e nomes de pasta de spec em inglês; comentários de
  código em português.
- **Backlog vive no GitHub Project `@ludens`** (`gcarvalhow` #2), não nos repos.

## Contribuindo neste repo

Este repo também segue o próprio fluxo TBD (`core` inclui as skills `tbd-*`) —
branch curta, PR pequeno, merge frequente em `master`. Issues e board no
[Project "@ludens"](https://github.com/orgs/gcarvalhow/projects/2).
