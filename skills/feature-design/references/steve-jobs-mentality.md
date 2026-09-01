# Mentalidade Steve Jobs — Guia de Pensamento de Produto

## Aviso de uso

Este documento não é uma biografia. Não é uma lista de frases motivacionais. É um
guia de raciocínio para quem está tomando decisões de produto no Ludens. Leia
antes de propor qualquer feature, corte de escopo, ou mudança de direção. Se você
não consegue defender sua ideia à luz deste guia, provavelmente ela não está
pronta.

---

## 1. O produto é a experiência, não o software

Steve Jobs não pensava em features. Ele pensava em experiências. A pergunta que
ele fazia não era "o que esse software faz?" mas sim "o que o usuário sente
quando usa isso?"

Isso muda tudo. Quando você pensa em features, você pensa em caixas de
funcionalidade que somam umas às outras. Quando você pensa em experiência, você
percebe que mais caixas muitas vezes pioram a experiência — porque adicionam
fricção, confusão, sobrecarga cognitiva.

Para o Ludens: a pessoa que quer assistir a uma peça abre o site e deve sentir,
em segundos, "achei, tem lugar, é meu". Não deve sentir que está preenchendo um
formulário burocrático, que precisa entender um mapa de assentos complicado, ou
que corre o risco de o ingresso sumir enquanto paga. Deve sentir alívio e
controle: a compra é simples, a reserva é garantida enquanto ela paga, a
confirmação chega.

Toda decisão de produto precisa ser testada contra esse critério: isso aumenta o
senso de "achei e é meu", ou aumenta o ruído?

---

## 2. Produto primeiro. Engenharia depois.

Um dos erros mais comuns em times de tecnologia é deixar a engenharia guiar o
produto. Quando a engenharia guia o produto, o resultado é features que existem
porque eram fáceis de implementar, não porque o usuário precisava delas.

Jobs tinha a ordem invertida. Ele definia a experiência que queria criar. Definia
o que o usuário deveria sentir. Depois entregava para a engenharia descobrir como
fazer aquilo acontecer.

Isso não é ignorância técnica. É clareza de prioridade. Engenheiros brilhantes
constroem coisas extraordinárias quando o objetivo está claro. O que os
desorienta é quando o objetivo muda de "criar a melhor experiência possível" para
"implementar o que é tecnicamente mais conveniente agora".

Para o Ludens: quando você define uma feature, a pergunta não é "como
implementamos a reserva temporária?" A pergunta é "o que a pessoa sente entre
clicar em comprar e receber o ingresso — e como garantimos que ela nunca perde o
assento por causa de um detalhe técnico?" Depois que essa resposta está clara, a
implementação é problema de engenharia.

---

## 3. Simplicidade não é ausência de complexidade. É maestria sobre ela.

Jobs dizia que simplicidade é a sofisticação suprema. Isso é frequentemente mal
interpretado como "faça coisas simples e preguiçosas". Não é isso.

Simplicidade é o resultado de eliminar tudo que não é essencial até que o que
sobra seja exatamente o que precisa estar ali. Isso exige mais trabalho, não
menos. Mais decisões difíceis. Mais coragem para dizer não.

Um produto simples é aquele onde o usuário nunca fica em dúvida sobre o que
fazer. Onde a interface guia sem precisar explicar. Onde cada elemento tem um
propósito claro.

Para o Ludens: cada campo a mais no checkout, cada opção de filtro, cada etapa
entre descobrir o espetáculo e receber a confirmação é uma decisão que precisa
ser justificada. O critério de sucesso do produto é o caminho feliz em **≤ 5
passos** (RNF04). Se uma feature adiciona um passo, ela precisa remover fricção
maior do que a que cria.

---

## 4. O que você não constrói é tão importante quanto o que você constrói

Jobs era famoso por dizer não. Para features. Para produtos. Para ideias que
pareciam boas mas não eram essenciais. Quando voltou para a Apple em 1997, cortou
dezenas de produtos para quatro — com a empresa quase falindo.

Dizer não não é fraqueza ou falta de visão. É uma forma de proteção. É garantir
que o time tenha foco suficiente para fazer poucas coisas extraordinariamente
bem, em vez de muitas coisas de forma medíocre.

Para o Ludens: o MVP é N1 — cadastro de espetáculo e sessão, mapa simplificado
(setores A/B/C), compra inteira/meia. Scanner na porta e relatórios de ocupação
são N2/N3, e a bilheteria física presencial fica permanentemente fora. Uma
feature de N2 que você não constrói agora não é uma feature perdida — é uma
feature que não vai distrair do que faz o produto existir: nunca vender o mesmo
assento duas vezes.

---

## 5. Coerência de produto: cada peça fortalece o todo

Um produto não é a soma das suas features. É o resultado da interação entre elas.
Features que parecem independentes criam padrões de uso, expectativas, modelos
mentais. Uma feature que não se encaixa fragmenta o modelo mental do usuário.

Antes de adicionar uma feature, pergunte como ela conversa com as existentes —
não só tecnicamente, mas experiencialmente.

Para o Ludens: a disponibilidade em tempo real que a pessoa vê no detalhe da
sessão (RF02), a reserva temporária que segura o assento no checkout (RF03), a
liberação automática quando o pagamento não completa (RN03) e o histórico com
status (RF06) são a mesma promessa vista de ângulos diferentes: "o que você vê é
verdade, e o que é seu continua seu". Uma feature nova que quebre essa promessa
em algum ponto está fragmentando o produto, mesmo que funcione isolada.

---

## 6. Protótipos mentais: sinta antes de construir

Jobs simulava a experiência na cabeça antes de qualquer linha de código. Você
pode fazer o mesmo. Antes de aprovar uma feature, simule o uso real:

- Como o usuário descobre essa feature?
- O que ele vai tentar fazer primeiro?
- Onde ele vai travar?
- Como ele vai saber que completou a tarefa?
- Como ele vai se sentir depois?

Se você não consegue simular essa jornada de forma fluida na cabeça, a feature
não está definida o suficiente para ser construída.

Para o Ludens: simule uma pessoa comprando dois ingressos (um inteira, um meia)
para a sessão de sábado, no celular, dez minutos antes de sair de casa. Se ela
trava em qualquer ponto — não entende o setor, não sabe se a reserva está
valendo, não sabe quanto tempo tem para pagar, não recebe a confirmação — a
feature precisa ser repensada.

---

## 7. Não pergunte ao usuário o que ele quer. Entenda o que ele precisa.

Usuários são ótimos para descrever problemas e péssimos para propor soluções.
Quando alguém diz "quero um PDF do ingresso", o que quer é ter prova de que
comprou, para mostrar na entrada. O PDF é uma solução que ele imaginou. O
problema real pode ter soluções melhores (um código único, um QR na área do
usuário, um e-mail que não pode ser invalidado por falha de envio — RF05).

Interprete o feedback no nível certo: qual dor está tentando eliminar? Qual
insegurança está tentando resolver?

Para o Ludens: quando o teatro pede "um jeito de ver quantos ingressos já
venderam", o problema real muitas vezes é a ansiedade de não saber se a sessão
vai lotar ou encalhar. A solução pode ser um número de ocupação por sessão (N2),
não necessariamente uma tela nova de BI.

---

## 8. Qualidade não é negociável. Nunca.

Jobs mandava refazer produtos que para qualquer outra pessoa estariam prontos.
Isso não é perfeccionismo paralisante — é que quando algo não está certo, você
não deixa passar. "Bom o suficiente" é o início do declínio de um produto.

Para o Ludens: uma reserva que expira sem avisar a pessoa, uma mensagem de erro
com stack trace, um assento que "some" durante o pagamento e volta depois, um
e-mail de confirmação que às vezes não chega e invalida a compra — nada disso é
"bug menor". É falha de produto. Qualidade aqui não é polimento visual; é não
aceitar fricção que você tem poder de remover, e não deixar a pessoa insegura
sobre se comprou ou não.

---

## 9. O lançamento certo > o lançamento rápido

Jobs nunca lançou um produto porque estava "pronto o suficiente". Lançou quando a
experiência estava certa. O iPhone lançou sem 3G, sem copy-paste, sem App Store —
mas com a melhor experiência do mundo dentro do que fazia.

Fazer menos e fazer extraordinariamente bem é superior a fazer mais e fazer
medíocre. Mas esperar demais também tem custo: o produto não chega, o feedback
não acontece.

Para o Ludens: a primeira vez que o teatro adota a plataforma como fonte única de
disponibilidade, a experiência precisa criar confiança imediata. Se a primeira
sessão vendida online tiver um overbooking, a plataforma perde a razão de existir
aos olhos de quem a adotou. Priorize a robustez do caminho de compra (RF01→RF05,
RN05) acima de qualquer lista de features acessórias.

---

## 10. Custo de produto é parte da decisão de produto

Jobs pensava em produtos de forma holística — incluindo custo. Não só de
desenvolvimento: custo de manutenção, de suporte, de complexidade cognitiva, e
quando relevante de serviços externos.

Para o Ludens: o pagamento depende do AbacatePay (Pix) e a confirmação depende de
um serviço de e-mail transacional. Uma feature que adicione um novo provedor
externo (SMS, WhatsApp, outro gateway) é uma decisão de produto: o valor que cria
justifica o custo recorrente e a nova dependência? Existe degradação graciosa se
o provedor cair (RNF03)? Isso precisa estar respondido antes de a feature ir para
engenharia.

---

## 11. A jornada importa tanto quanto o destino

Jobs se importava com cada detalhe da jornada — não só com o resultado. Onboarding
ruim mata produtos. Loading states mal pensados criam ansiedade. Mensagens de erro
genéricas frustram.

Para o Ludens: a jornada de "quero ver essa peça" até "ingresso no meu e-mail e na
minha área" tem dezenas de pontos de contato — a busca, o filtro, o detalhe da
sessão, a escolha de quantidade e tipo, a reserva, o Pix, a espera pela
confirmação, o e-mail. Cada um importa. Um contador regressivo claro na reserva,
um estado de "pagamento em processamento" honesto, um erro que diz o que fazer —
não são detalhes, são a diferença entre confiar e não confiar no produto.

---

## 12. Produto para pessoas reais em situações reais

Jobs imaginava o usuário em contexto real — apressado, sobrecarregado, usando o
produto em 30 segundos entre uma coisa e outra. Não o usuário de laboratório.

Para o Ludens: o comprador típico é alguém decidindo de última hora, no celular,
sem paciência para aprender uma interface. O admin do teatro é alguém que
cadastra sessões entre um ensaio e outro. Qualquer feature que exija treinamento,
qualquer interface que exija aprender uma lógica nova, tem custo de adoção alto
demais para esse perfil. Responsividade e acessibilidade (WCAG 2.1 AA, RNF04) não
são enfeite — mobile é pré-requisito do próprio N2.

---

## 13. Não construa features. Resolva problemas.

Features são soluções sem problema definido. "Vamos adicionar um histórico de
atividades." Por quê? Para quê? Quem precisa?

Problemas são o ponto de partida correto. "A pessoa não sabe se a compra foi
confirmada e liga para o teatro." Agora você tem um problema real, e a solução
pode ser um status visível no histórico, um e-mail, um reenvio de ingresso — o
problema guia a decisão.

Para o Ludens: antes de propor qualquer feature, defina o problema. Quem tem?
Com que frequência? Qual o impacto? O que fazem hoje para contornar? Sem problema
claro, a feature é só ruído no produto.

---

## 14. Integridade do produto ao longo do tempo

Cada decisão de hoje afeta as de amanhã. Uma feature mal projetada cria dívida de
produto, expectativas difíceis de reverter, padrões de interface que se propagam.

Para o Ludens: o produto de longo prazo é "o sistema operacional da bilheteria do
teatro" — catálogo, venda, validação na porta, ocupação. Features de N1 precisam
parecer projetadas junto com as de N2/N3, não empilhadas. O modelo de sessão,
ingresso e ordem que o N1 fixa é a fundação de tudo que vem depois.

---

## 15. Perguntas obrigatórias antes de aprovar qualquer feature

Antes de considerar uma feature aprovada para desenvolvimento, responda:

1. Que problema específico e real essa feature resolve?
2. Para quem exatamente? Em qual momento da jornada?
3. Como o usuário resolve esse problema hoje sem a feature?
4. O que você vai remover ou simplificar para acomodar essa feature?
5. Como essa feature conversa com o que já existe no produto?
6. O que essa feature abre para o futuro?
7. O que essa feature pode fechar ou complicar no futuro?
8. Se você pudesse lançar a metade dessa feature, qual metade seria?
9. Existe um custo externo (serviço, API, infraestrutura) para essa feature?
10. Como o usuário descobre essa feature sem ser ensinado?

Se você não tem resposta clara para pelo menos 8 dessas 10, a feature não está
pronta para ser aprovada.

---

## 16. O que Jobs pensaria sobre o Ludens

**O que ele diria que está certo:**
- Fonte única de disponibilidade como razão de existir — clara, verificável,
  imediata.
- Reserva temporária garantida no checkout — protege o usuário do pior momento
  do fluxo.
- Focar no comprador e no pequeno teatro como usuários primários — quem tem a dor
  real.

**O que ele provavelmente questionaria:**
- A pessoa entende o mapa de setores de primeira, sem legenda?
- O que acontece quando o Pix demora — a pessoa sabe que está tudo bem?
- A primeira compra online do teatro cria uma sensação de "isso funciona"?
- O admin consegue cadastrar uma sessão inteira sem manual?

**O que ele diria sobre o roadmap:**
- N1 antes de scanner na porta: certo. Não dá pra validar na entrada o que não
  foi vendido de forma confiável.
- Relatórios de ocupação depois do scanner: certo. O dado bom vem da porta.

---

## 17. Resumo executivo

Se você vai lembrar apenas de uma coisa deste documento:

**Produto é o que o usuário sente. Engenharia é como você faz ele sentir isso.**

Comece sempre pelo sentimento que você quer criar. Depois construa o caminho para
chegar lá. Nunca ao contrário.

E quando estiver em dúvida sobre incluir ou não uma feature: não inclua. O
produto sempre fica melhor quando você remove do que quando você adiciona.
