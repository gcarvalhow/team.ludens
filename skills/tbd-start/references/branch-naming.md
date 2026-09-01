# Como gerar o slug da branch

Issues são em português; a branch é **sempre em inglês**. Isso exige tradução,
não transliteração — não basta tirar acento das palavras em português.

O número da issue já aparece no começo da branch e já é o elo de rastreio
completo (`gh issue view {número}` traz todo o contexto) — o slug não precisa
recontar a issue inteira, só dar um rótulo objetivo pra reconhecer a branch de
relance.

1. Pegue o assunto coletado no passo 1 (já em português)
2. Reduza ao núcleo do objetivo: 2–3 palavras-chave, corte
   artigos/preposições/palavras de encheção
3. Traduza o sentido pro inglês técnico (traduza de verdade — palavras
   portuguesas sem acento não valem como slug em inglês)
4. Gere o slug: tudo minúsculo, espaços viram hífens, remova caracteres
   especiais, máximo 20 caracteres
5. Monte: `{tipo}/{número}-{slug}`, usando o mesmo `{tipo}` do passo 1 e o número
   da issue recém-criada

Exemplos:
- assunto `reserva temporária de ingressos com expiração`, tipo `feat`, issue `#7` → `feat/7-ticket-reservation`
- assunto `busca e filtro de espetáculos por data e gênero`, tipo `feat`, issue `#3` → `feat/3-show-search`
- assunto `pagamento pix via abacatepay`, tipo `feat`, issue `#12` → `feat/12-pix-checkout`
- assunto `corrigir cálculo de reembolso fora da janela de 24h`, tipo `fix`, issue `#20` → `fix/20-refund-window`
- assunto `documentar o pipeline de specs`, tipo `docs`, issue `#8` → `docs/8-spec-pipeline`
