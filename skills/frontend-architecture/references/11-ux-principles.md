# Princípios de UX

Fazem parte do contrato de entrega, não são opcionais. Fonte cruzada:
`docs.ludens/requirements/overview.md` (RNF04) + a mentalidade Steve Jobs da skill
`feature-design`.

## 1. Estados assíncronos — sempre loading, error e empty

- **Loading:** skeleton com a mesma estrutura dimensional do conteúdo real
  (não um retângulo genérico). Spinner só para ação pontual (botão de submit).
  Nunca tela em branco/congelada.
- **Error:** mensagem amigável em pt-BR. Nunca chave técnica, código de status ou
  stack trace. Sempre uma ação de recuperação ("Tentar novamente", "Voltar"). Erro
  de permissão (401/403): redirecionar ou explicar que o acesso não é permitido.
- **Empty:** mensagem útil e específica do contexto ("Você ainda não fez nenhuma
  compra"), com CTA quando fizer sentido. Distinguir de loading — nunca mostrar
  empty enquanto carrega.

## 2. O caminho feliz cabe em ≤ 5 passos

Descoberta → confirmação em no máximo 5 passos (RNF04). Cada passo que uma feature
adiciona precisa remover fricção maior do que a que cria. Comprador típico: no
celular, decidindo de última hora, sem paciência para aprender.

## 3. Formulários

- Validar **no submit** por padrão (`mode: 'onSubmit'`). Blur só para campos com
  feedback em tempo real (CPF com dígito verificador, e-mail com verificação de
  disponibilidade). Nunca on-keystroke em campo simples.
- Mensagens de erro em pt-BR, específicas ao campo ("CPF inválido", não "Campo
  inválido"), abaixo do campo com `<FormMessage />`. Nunca alert/modal para erro
  de validação de campo.
- Submit: botão com estado de loading (`{isPending ? 'Salvando...' : 'Salvar'}`),
  desabilitado durante `isPending` (sem double submit). Após sucesso: resetar o
  form, fechar o dialog, toast.

## 4. Feedback de mutations

- Feedback imediato: UI otimista (quando previsível e com rollback) **ou** loader
  no botão. Nunca otimismo em disponibilidade de assento (RN05).
- **Toasts: sempre sucesso E erro**, nunca só um. `sonner`, posição topo-direito
  (config global no `<Toaster />`). Curtos (≤ 2 linhas), pt-BR, específicos, sem
  jargão técnico.

## 5. Mensagens de erro específicas e acionáveis

- ❌ "Erro 409: reservation constraint violated"
- ✅ "Não há mais ingressos disponíveis para esta sessão."
- ✅ "Você já atingiu o limite de 6 ingressos por sessão."

Nunca vazar dado pessoal (CPF, e-mail) em erro ou URL (RNF01).

## 6. A reserva sempre mostra quanto tempo resta

Onde há reserva ativa, o tempo restante até `expiresAt` é visível e honesto. Ao
zerar, a pessoa vai para um estado claro ("a reserva expirou, os ingressos
voltaram para a sessão, você pode reservar de novo"), nunca um erro genérico. RN03.

## 7. Pagamento Pix: a espera é honesta

Entre "paguei" e "confirmado" há uma janela (webhook do AbacatePay + ~2 s do relay
do backend). A tela de "aguardando confirmação" diz isso com tranquilidade, faz
polling do status, e quando confirma leva direto ao ingresso. Se falhar, a reserva
é liberada e a pessoa sabe que pode tentar de novo (RF04).

## 8. Navegação — nunca deixar o usuário preso

- Toda tela tem caminho de volta (breadcrumb, botão Voltar, link).
- Toda dialog/sheet tem fechar explícito (X ou "Cancelar").
- Toda ação destrutiva (cancelar pedido, cancelar sessão) tem confirmação com
  `AlertDialog` e caminho de cancelar.
- **Proibido**: `window.confirm()`, `window.alert()`, `window.prompt()`.
- Após criar: redirecionar ao detalhe OU fechar dialog e atualizar lista. Após
  cancelar/excluir: voltar à lista OU fechar dialog e remover da lista.

## 9. Acessibilidade (WCAG 2.1 AA)

- Todo interativo com nome acessível (`aria-label` quando sem texto visível).
- `<label>` associado a cada input (via `htmlFor` ou `<FormItem>`); nunca
  placeholder como label. Erro associado via `aria-describedby` (o `<FormMessage />`
  do shadcn/ui faz isso).
- Foco: ao abrir dialog/sheet vai para o primeiro focável; ao fechar volta ao
  elemento que abriu; trap de foco em modais (Radix trata).
- Navegação por teclado, contraste, foco visível; `alt` na imagem do espetáculo.

## 10. Responsividade

- Funciona em **375px** (mobile) e **1024px+** (desktop). Mobile-first, classes
  Tailwind responsivas (`sm:` `md:` `lg:`).
- Botões com área de toque ≥ 44×44px (`min-h-11 min-w-11`). Inputs nunca menores
  que a fonte base (evita zoom do iOS). Listas longas scrolláveis, não cortadas.
- Mobile é pré-requisito do N2 (scanner na porta) — o layout funciona no celular
  desde o N1.

## 11. Confirmação que não pode ser perdida

O e-mail de confirmação pode falhar sem invalidar a compra (RF05) — então o
ingresso (código único / QR) **sempre** aparece em "Minhas compras", e de lá dá
para reenviar o e-mail. A área do usuário é a fonte, o e-mail é a conveniência.
