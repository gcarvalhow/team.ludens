---
name: setup
description: Verifica se o ambiente local (git, gh, python) está pronto pra usar o plugin team-ludens neste repo, e aponta a correção exata pro que faltar. Use depois de instalar o plugin num repo novo, ou quando o lembrete de SessionStart avisar que o setup ainda não foi validado aqui.
allowed-tools: Bash(python "${CLAUDE_SKILL_DIR}/scripts/check_environment.py":*)
disallowed-tools: Write, Edit, Bash(git push:*), Bash(git commit:*)
---

Checagem read-only de ambiente — não muta nada no repo do usuário. A única
escrita é o marcador de "setup validado" (feito pelo próprio script, em
`${CLAUDE_PLUGIN_DATA}`, ou em `~/.claude/team-ludens/data` se essa variável não
estiver disponível), e só depois que tudo obrigatório passa.

**1. Rodar a checagem** — `${CLAUDE_SKILL_DIR}/scripts/check_environment.py` (um
`python` só).

**2. Mostrar o relatório completo** ao usuário, na íntegra — não resuma nem
filtre linhas, inclusive os itens que já passaram.

**3. Se algo obrigatório faltar** — aponte a linha de remediação que o próprio
script já imprimiu. Não tente corrigir automaticamente (`gh auth login` é
interativo). Sugira rodar `/team-ludens:setup` de novo depois da correção.

**4. Se tudo obrigatório passou** — informe que o marcador foi salvo (o lembrete
de SessionStart não aparece mais pra este repo) e sugira o próximo passo:
`/team-ludens:tbd-scope` (se o pedido precisa de escopo/grounding),
`/team-ludens:feature-design` (se é uma feature de produto nova) ou direto
`/team-ludens:tbd-start`.
