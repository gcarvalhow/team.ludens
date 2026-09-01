# Princípios de UX

Fonte: `docs.ludens/requirements/overview.md` (RNF04) + a mentalidade Steve Jobs
da skill `feature-design`.

## O caminho feliz cabe em ≤ 5 passos

Descoberta → confirmação em no máximo 5 passos (RNF04). Cada passo que uma feature
adiciona precisa remover fricção maior do que a que cria. O comprador típico está
no celular, decidindo de última hora, sem paciência para aprender.

## Todo estado assíncrono tem loading, error e empty

Nada de tela em branco enquanto carrega. Nada de crash em erro. Nada de lista
vazia sem mensagem que diga o que fazer. Isso vale para toda query.

## Mensagens de erro são específicas e acionáveis, sem detalhe técnico

- ❌ "Erro 422: reservation constraint violated"
- ✅ "Não há mais ingressos disponíveis para esta sessão."
- ✅ "Você já atingiu o limite de 6 ingressos por sessão."

Nunca vazar stack trace, nome de campo interno, ou id técnico numa mensagem
visível (RNF01 também: nada de dado pessoal em erro/URL).

## A reserva sempre mostra quanto tempo resta

Onde há uma reserva ativa, o tempo restante até expirar é visível e honesto. Ao
zerar, a pessoa vai para um estado claro ("a reserva expirou, os ingressos
voltaram para a sessão — você pode reservar de novo"), nunca um erro genérico.
RN03.

## Pagamento Pix: a espera é honesta

Entre "paguei" e "confirmado" há uma janela (webhook do AbacatePay + ~2s do relay
do backend). A tela de "aguardando confirmação" diz isso de forma tranquila, faz
polling do status, e quando confirma leva direto ao ingresso. Se falhar, a
reserva é liberada e a pessoa sabe que pode tentar de novo (RF04).

## Responsivo e acessível

Mobile é pré-requisito do N2 (scanner na porta) — o layout funciona bem no
celular desde o N1. WCAG 2.1 AA como referência: navegação por teclado,
contraste, foco visível, `alt` em imagem de espetáculo, labels associados a
inputs.

## Confirmação que não pode ser perdida

O e-mail de confirmação pode falhar sem invalidar a compra (RF05) — então o
ingresso (id único / QR) **sempre** aparece na área "Minhas compras", e de lá dá
para reenviar o e-mail. A área do usuário é a fonte, o e-mail é a conveniência.
