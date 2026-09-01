---
name: feature-design
description: >
  Skill de planejamento de produto para o Ludens. Use para decidir se uma feature
  deve ser construída, definir o que ela deve ser, entender como se conecta ao
  produto, ou gerar uma spec de produto. Produto primeiro — sem código, sem
  arquitetura, sem stack.
user-invocable: true
argument-hint: "[nome da feature ou descrição do problema]"
---

# Feature Design

Essa skill pensa em features da mesma forma que Steve Jobs pensava em produtos.

Produto primeiro. Engenharia resolve o resto.

Antes de uma única linha de código ser escrita, antes de qualquer decisão de
arquitetura, antes de qualquer sprint ser planejado — essa skill responde à
pergunta que mais importa: **isso deve existir e, se sim, o que exatamente deve
ser?**

---

## Leitura obrigatória antes de pensar

Carregue estes documentos antes de responder. Leia-os por completo.

1. `docs.ludens/product/problem.md` — o problema (venda duplicada de assento,
   ausência de fonte única de disponibilidade) e os critérios de sucesso
2. `docs.ludens/product/scope.md` — dentro/fora de escopo, níveis N1/N2/N3, premissas
3. `docs.ludens/requirements/functional.md` e `.../business-rules.md` — RF01–RF09
   e RN01–RN05 (aprovados pelo PO em 2026-08-28)
4. `references/steve-jobs-mentality.md` — o framework de pensamento de produto

Não prossiga sem ler os quatro.

---

## O que essa skill faz

Produz um documento de especificação de produto para uma feature. Não produz
planos técnicos, guias de implementação ou decisões de arquitetura. Tudo no
output é escrito na linguagem do usuário e do produto, não na linguagem de
engenheiros.

---

## Processo de pensamento (executar internamente antes de escrever)

Esta skill trata cada invocação como ponto de partida completo. Não pressuponha
que quem a invocou já fez análise de fit, dependências ou perguntas Steve Jobs.

**1. Qual é o problema real?**
Não o que a feature faz. Que problema ela resolve. Quem tem esse problema (o
comprador? o PO/admin do teatro?). Com que frequência. O que fazem hoje pra
contornar. Se é um problema que vale resolver agora ou depois.

**2. Isso se encaixa no produto?**
Usando `product/problem.md`, `product/scope.md` e `requirements/*`: onde essa
feature se posiciona? É N1 (MVP) ou N2/N3? Ela fortalece a "fonte única de
disponibilidade" ou adiciona ruído? De quais features/módulos depende? Quais
habilita?

**3. Qual é a pergunta Steve Jobs?**
De `references/steve-jobs-mentality.md`: execute as 10 perguntas obrigatórias. Se
não conseguir responder pelo menos 8 com clareza, diga isso no documento de
output e marque a feature como precisando de mais definição antes de ser aprovada.

**4. Qual é a versão mínima que importa?**
A menor versão que genuinamente resolve o problema — a que faria um usuário dizer
"finalmente". Não a visão completa.

**5. Existem custos além de código?**
Serviços externos (AbacatePay, provedor de e-mail transacional), armazenamento,
qualquer coisa com custo recorrente ou nova dependência. Se sim, quais as
implicações.

---

## Formato do output

Gere um documento markdown e salve em:

```
docs.ludens/specs/[domain]-[concept]/spec.md
```

### Convenção de nomenclatura obrigatória

- `[domain]` é sempre um dos módulos do produto: `identity`, `catalog`,
  `booking`, `payment`, `notification`
- `[concept]` é o nome curto da feature, kebab-case, máximo 2 palavras, em inglês
- Nomes de pasta e arquivo sempre em inglês; o conteúdo do documento sempre em português

Exemplos corretos:
```
docs.ludens/specs/booking-reservation/spec.md
docs.ludens/specs/catalog-show-search/spec.md
docs.ludens/specs/payment-pix-checkout/spec.md
docs.ludens/specs/identity-auth/spec.md
```

Nunca usar caminhos planos (`specs/[feature-name].md`). Nunca sufixos como
`-impact`, `-contract`, `-v2` no nome da pasta.

### Frontmatter obrigatório

```yaml
---
status: draft
domain: booking
created_at: 2026-09-01
---
```

Adicionar `approved_at` somente quando o PO aprovar explicitamente, e mudar
`status` para `approved`. Valores de `status`: `draft` | `approved` |
`in-progress` | `done` | `archived`. Nunca marcar `approved` sem confirmação
direta do PO.

### Seções do documento

1. **Visão da feature** — 1 a 3 parágrafos na linguagem do usuário. O que é, como
   percebe, o que permite. Sem linguagem técnica.
2. **Problema que resolve** — específico e real. Não vago.
3. **Para quem é** — beneficiário direto e indireto, perfil, momento da jornada.
4. **Como melhora a experiência atual** — antes e depois.
5. **Como se conecta com o produto existente** — dependências obrigatórias, o que
   habilita, posição no produto (core / complementar), RF/RN cobertos.
6. **O que não é (escopo negativo)** — o que está explicitamente fora. Cada item
   começa com "Não é" ou "Não inclui" + justificativa. Ao menos um item.
7. **Custos adicionais** — serviços externos, APIs, armazenamento. Ou
   explicitamente: "Nenhum custo externo identificado."
8. **Decisões tomadas** — tabela `| Ponto | Decisão |`. Cresce a cada iteração.
9. **Perguntas abertas** — decisões não resolvidas. Se nenhuma:
   "Nenhuma. Todas as decisões de produto estão fechadas." Nunca omitir.

---

## Proibições absolutas

Nunca incluir no output: trechos de código; schemas de banco; contratos de API ou
endpoints; decisões de arquitetura; referências a stack; nomes de componentes ou
caminhos de arquivo; cronogramas de implementação; atribuições de sprint.

---

## Checagem final antes de salvar

1. Uma pessoa não-técnica consegue ler e entender completamente a feature?
2. Todas as seções falam a linguagem do usuário?
3. O problema é específico o suficiente pra validar com um usuário real?
4. O escopo negativo tem ao menos um item relevante?
5. Se há custos, eles estão em termos de negócio?

Se qualquer resposta for não, revise antes de salvar. Depois de salvar, a spec
vai para **aprovação humana do PO** antes de qualquer artefato subsequente
(`logic.md`).
