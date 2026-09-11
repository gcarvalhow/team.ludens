## O quê
<!-- O que foi implementado/alterado — seja objetivo -->

## Por quê
<!-- Motivação e contexto; referencie a issue e a spec quando relevante -->

## Notas ao revisor
<!-- Opcional — decisões de design, breaking changes, pontos de atenção.
Em mudanças de frontend/UI, considere trocar por "## Como testar" com passos de
verificação manual quando ajudar o revisor. -->

## Definition of Done
- [ ] Revisão de conformidade rodada nesta branch (`senior-dev` Modo 2 +
  `/code-review`, guia de estilo `docs.ludens/backend/code-style.md` e
  `docs.ludens/backend/conventions.md`) — achados endereçados, ou pulo
  justificado acima em "Notas ao revisor"
- [ ] Code Review — este PR aprovado por ≥ 1 outro desenvolvedor
- [ ] Validado e testado conforme a estratégia de QA, sem erros críticos
- [ ] Testes automatizados relevantes criados/atualizados e passando no pipeline
- [ ] Integra em `master` sem quebrar o build (lint + testes + Docker build verdes)

Closes #{número}
