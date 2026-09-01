---
name: tbd-commit
description: Gera um commit no padrão Conventional Commits a partir do que está staged. Use quando o usuário quiser commitar.
allowed-tools: Bash(git status:*), Bash(git diff:*), Bash(git branch:*), Bash(git commit:*)
disallowed-tools: Bash(git add:*)
---

**1. Estado do repo** — `git status` e `git diff --staged`. Se nada staged:
mostre `git diff`, pergunte o que incluir. **Nunca rode `git add`
automaticamente.**

**2. Tipo** — leia a branch (`git branch --show-current`) e mapeie:
`feat/`→`feat`, `fix/`→`fix`, `refactor/`→`refactor`, `test/`→`test`,
`infra/`→`chore`, `docs/`→`docs`. Sem prefixo reconhecido: pergunte. O prefixo é
padrão, não absoluto — se o diff staged claramente não bate (branch `feat/` mas
só corrige algo quebrado), avise e pergunte qual tipo usar.

**3. Escopo** — veja `references/scope-detection.md` (detecção dinâmica, sem lista
fixa; inclui a regra de parar se há assuntos misturados).

**4. Mensagem** — `{tipo}({escopo}): {descrição imperativa, presente, minúscula,
sem ponto final}`, em português, máx. 72 caracteres. Nunca use termos vazios
(`update`, `ajustes diversos`, `wip`) — descreva o efeito real. Corpo opcional
após linha em branco se houver contexto relevante.

**5. Confirmar** — mostre a mensagem, pergunte antes de commitar.

**6. Commit** — `git commit -m "{mensagem confirmada}"`.
