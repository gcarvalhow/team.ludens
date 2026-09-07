# Como decidir Priority

Convenção do Project `@ludens` (espelha a de um sistema de automação privado
anterior do mesmo autor):
**quanto maior o número, mais importante** — o oposto do estilo "P0 é o mais
urgente". `0` é o piso da escala; não force um valor nele sem um sinal explícito
de que é rascunho/exploração sem compromisso de entrega.

Decida por julgamento — o mesmo raciocínio já usado pra escrever a seção "Por
quê" da issue — olhando o **impacto/raio de alcance** da mudança, não o `{tipo}`
sozinho (um `docs` pequeno e um `docs` que reescreve uma seção inteira não têm o
mesmo peso). **Nunca pergunte ao usuário.**

## A escala

- **`3`** — impacto largo: domínio central do produto, feature ponta-a-ponta
  (RF01–RF09), validação essencial, regra de negócio de segurança/consistência
  (RN05 disponibilidade atômica, RN01 limite por CPF, RN03 expiração de reserva,
  RN02 reembolso), pipeline/CI, bug que bloqueia compra ou pagamento ou expõe
  dado pessoal.
- **`2`** — mudança contida de médio porte: refactor que toca vários arquivos
  mas não o núcleo do domínio, feature secundária, habilitação de config/tooling
  que afeta todo mundo que usa o repo (mas não é produto em si), integração com
  serviço externo não-crítico.
- **`1`** — pequena, mecânica, ou tooling interno do próprio `team.ludens`:
  link/README quebrado, remover arquivo morto, renomear, dedupe de uma função
  isolada, ajuste pontual em skill/agent, correção de texto em doc.
- **`0`** — só trabalho exploratório/rascunho sem compromisso de entrega.
  Reservado, não é gatilho default.

## Depois de decidir

Informe o valor escolhido **com uma linha de justificativa** no passo de
confirmação ("Confirmar") — não é uma pergunta, é parte do resumo final, pra o
usuário conseguir corrigir se discordar.
