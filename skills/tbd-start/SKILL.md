---
name: tbd-start
description: Inicia uma nova task TBD — cria a issue, linka no Project @ludens e cria a branch no mesmo fluxo. Use ao começar a trabalhar em algo novo.
argument-hint: [do que se trata]
allowed-tools: Bash(gh issue list:*), Bash(gh issue create:*), Bash(gh issue edit:*), Bash(gh project item-add:*), Bash(gh project item-edit:*), Bash(gh repo view:*), Bash(git checkout *), Bash(git pull:*)
---

Fluxo Trunk Based Development: cria a issue, linka no Project e cria a branch
juntas.

Repo atual: !`gh repo view --json nameWithOwner -q .nameWithOwner` (chame o resultado de `{repo}`)

**1. Coletar** — tipo (`feat`/`fix`/`refactor`/`test`/`infra`/`docs`) e do que se
trata (breve, você desenvolve o resto do contexto). $ARGUMENTS já pode trazer isso.
Se a task nasce de uma spec (`docs.ludens/specs/[domínio]-[conceito]/`):

- **Antes de citar a pasta, atualize `docs.ludens` e confira se a spec mudou
  recentemente.** `git -C <caminho-local-de-docs.ludens> pull` (sem checkout
  local, releia o arquivo direto do GitHub — nunca confie em conteúdo já
  carregado na sessão). Depois `git -C <caminho-local-de-docs.ludens> log -1
  --format="%ci %s" -- specs/<pasta>/{spec,logic,integration,backend,frontend,quality}.md`
  em cada documento que a issue vai referenciar. Se o commit mais recente for
  de hoje ou dos últimos dias, releia o arquivo inteiro agora — não assuma que
  o que já foi consultado antes ainda é o texto atual.
  Isso existe porque `catalog-admin-management` (`api.ludens` PR #17) foi
  implementada contra uma versão de `backend.md` anterior a uma correção feita
  no **mesmo dia** — ninguém checou a data antes de começar.
- Cite a pasta no corpo da issue — referencia `spec.md` / `logic.md` e o
  documento da superfície (`backend.md` / `frontend.md` / `quality.md`).

**2. Checar duplicata** — `gh issue list --repo {repo} --state all --search
"{palavras-chave}"`. Se achar algo cobrindo o mesmo assunto: **pare**, mostre ao
usuário, só prossiga com confirmação de que é algo novo.

**3. Título** — `{tipo}: {título técnico, minúsculo após os dois-pontos, sem
ponto final}`, em português.

**4. Corpo** — use `templates/issue-body.md` (seções fixas). Se a task for uma
fatia de feature vinda de `backend.md` / `frontend.md` / `quality.md`, a seção
"Escopo" é a checklist de arquivos daquele documento, e "Referências" linka a
pasta de spec.

**5. Confirmar** — mostre título e corpo, pergunte antes de criar.

**6. Criar a issue** — `gh issue create --repo {repo} --title "{título}"
--body "{corpo}"`. Guarde a URL retornada (`{issue_url}`).

**7. Linkar no Project `@ludens`**

```
gh project item-add 2 --owner gcarvalhow --url {issue_url}
```

Derive os campos e confirme **Area** com o usuário antes de setar (Issue Type e
Priority são diretos, não precisam confirmação):

- **Area** — pelo repo, com exceção de `{tipo}`: se `{tipo}` for `infra` →
  `infra`; senão se `{tipo}` for `docs` ou o repo for `docs.ludens` → `docs`;
  senão se o repo for `web.ludens` → `frontend`; senão → `backend`.
- **Issue Type** — pelo `{tipo}`: `feat`→`feature`, `fix`→`bug`,
  `refactor`→`refactor`, `test`/`infra`/`docs`→`task`.
- **Priority** — decida sozinho, **sem perguntar ao usuário**: veja
  `references/priority-rubric.md` (escala `0`–`3`, quanto maior mais importante).

```
gh project item-edit --project-id <PVT_kwDODjbi-M4BiJU_> --id <ITEM_ID> --field-id <FIELD_ID> --single-select-option-id <OPT_ID>
```

> Na prática use a forma amigável quando o seu `gh` suportar:
> `gh project item-edit 2 --owner gcarvalhow --url {issue_url} --field "Area" --value "{area}"`
> (idem `Issue Type`, `Priority`). Se a forma amigável não existir na versão
> instalada, resolva os ids via `gh project field-list 2 --owner gcarvalhow --format json`.

**8. Labels da taxonomia Ludens** — `gh issue edit {issue_url} --add-label`:
- `module: {identity|catalog|booking|payment|notification}` quando a task toca um
  módulo do monólito (backend) ou a feature correspondente (frontend).
- `N1` / `N2` / `N3` conforme o nível de entrega da feature (`docs.ludens/product/scope.md`).
- `débito técnico` quando `{tipo}` cobre um atalho/refactor registrado.

**9. Nome da branch** — veja `references/branch-naming.md` (tradução pro inglês,
geração do slug, exemplos).

**10. Criar a branch** — `git checkout master && git pull && git checkout -b
{nome-da-branch}`.

**11. Confirmar** — informe issue + Project linkado (Area/Type/Priority, com uma
linha de justificativa pra Priority pro usuário corrigir se discordar) + labels +
branch criadas, e que o prazo é 2 dias para abrir o PR.
