---
name: tbd-pr
description: Abre PR quando a branch está pronta, ou finaliza o ciclo (limpa a branch local) quando o PR já foi mergeado — detecta o estado sozinho. Use ao terminar de trabalhar numa branch, e de novo depois que o PR for mergeado.
allowed-tools: Bash(gh issue view:*), Bash(gh pr list:*), Bash(gh pr create:*), Bash(gh repo view:*), Bash(git status:*), Bash(git push:*), Bash(git log:*), Bash(git diff:*), Bash(git branch:*), Bash(git checkout *), Bash(git pull:*), Agent(team-ludens:senior-dev)
---

Repo atual: !`gh repo view --json nameWithOwner -q .nameWithOwner` (chame de `{repo}`)
Branch atual: !`git branch --show-current` (chame de `{branch}`)

Se `{branch}` for `master`: **aborte**, oriente a usar `/team-ludens:tbd-start`.

**1. Descobrir o estado do PR desta branch**

```
gh pr list --repo {repo} --head {branch} --state all --json number,state,url,mergedAt --limit 1
```

- **Vazio** → siga o fluxo **Abrir PR**.
- **`state: OPEN`** → informe a URL e pare: "PR já aberto, aguardando review/CI."
- **`state: MERGED`** → siga o fluxo **Finalizar**.
- **`state: CLOSED` sem merge** → pare e pergunte ao usuário o que fazer.

## Fluxo: Abrir PR

Extraia tipo e número da issue do nome da branch (`{tipo}/{número}-{slug}`). Se
não seguir esse padrão: **aborte**, oriente `/team-ludens:tbd-start`.

1. `gh issue view {número} --repo {repo}` — se falhar, **aborte**. Salve o título.
2. `git status` — se houver mudança não commitada, sugira `/team-ludens:tbd-commit`.
3. **Rode, não pergunte se deve rodar**: `Agent(subagent_type: team-ludens:senior-dev)`
   (Modo 2, conformidade com a skill de arquitetura do repo) e a skill nativa
   `/code-review` (bugs/qualidade) sobre `git diff master...HEAD`, antes do push.
   Isto não é mais opcional por padrão — `catalog-admin-management` (PR #17) foi
   exatamente o caso que essa checagem deveria ter pego antes do review humano
   (`CamelModel`, VO `Money`, `find_by_id`/`find_by_id_for_update` inventados,
   rotas `PATCH` — tudo sem precedente no código já mergeado).
   - Achado de não-conformidade → mostre ao usuário, corrija antes de continuar.
   - Só pule a rodada se o usuário pedir explicitamente pra pular (branch
     trivial, doc-only, etc.) — registre esse pulo na "Notas ao revisor" do PR,
     não deixe implícito.
4. Confirme com o usuário antes de dar push.
5. `git push -u origin {branch}`.
6. Monte o corpo com `templates/pr-body.md`, com base em `git log
   master..HEAD --oneline` e `git diff master...HEAD`. Título = título exato da
   issue (já tem o prefixo `{tipo}:`, não concatene de novo).
7. **Mostre título e corpo gerados (incluindo o `Closes #{número}` e a checklist
   de DoD) e pergunte antes de criar.** Aplique qualquer edição pedida.
8. `gh pr create --title "{título}" --body "{corpo}" --repo {repo} --base master`.
9. Confirme a URL e lembre: depois do merge, rodar este mesmo skill de novo
   finaliza o ciclo. Merge exige 1 aprovação de outro dev + pipeline verde.

## Fluxo: Finalizar

1. `git checkout master && git pull`.
2. `git branch -d {branch}` (nunca `-D`; se o git recusar, avise o usuário e não
   force).
3. Confirme: ciclo encerrado, pronto para `/team-ludens:tbd-start`.
