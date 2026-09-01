# TEMPLATE — Spec de Produto (Ludens)

Modelo canônico para specs de produto do Ludens. Ao criar uma spec, salvar como
`docs.ludens/specs/[domínio]-[conceito]/spec.md`.

> Ler antes de escrever:
> - `docs.ludens/product/problem.md` — problema e critérios de sucesso
> - `docs.ludens/product/scope.md` — escopo e níveis N1/N2/N3
> - `docs.ludens/requirements/functional.md` e `.../business-rules.md` — RF/RN
> - `references/steve-jobs-mentality.md` — o framework de pensamento

---

## O que uma spec não é

- Não é um plano técnico
- Não é um guia de implementação
- Não é uma decisão de arquitetura
- Não é uma lista de endpoints
- Não é um schema de banco de dados
- Não é um cronograma de sprint

Uma pessoa não-técnica deve conseguir ler a spec e entender completamente a
feature. Se não conseguir, a spec está errada.

---

## Frontmatter obrigatório

```yaml
---
status: draft
domain: booking
created_at: 2026-09-01
---
```

Adicionar `approved_at` e mudar `status` para `approved` **somente** após
aprovação explícita do PO.

| Status | Significado |
|---|---|
| `draft` | Em elaboração, ainda não aprovada |
| `approved` | Aprovada pelo PO, pronta para o `logic.md` |
| `in-progress` | Aprovada e com implementação em andamento |
| `done` | Implementada com sucesso |
| `archived` | Descartada, não deve ser implementada |

Domínios válidos: `identity`, `catalog`, `booking`, `payment`, `notification`.

## Cabeçalho

```
# [Nome legível da feature]
```

---

## 1. Visão da feature

Um a três parágrafos, na linguagem do usuário: o que é, como o usuário a percebe
e experimenta, o que ela permite que ele faça que não conseguia antes. Sem
linguagem técnica, sem stack, sem endpoints.

## 2. Problema que resolve

Qual é o problema concreto no dia a dia do usuário; com que frequência acontece;
o que ele faz hoje pra contornar; por que esse workaround é insuficiente. Sem
linguagem vaga ("melhora a experiência"). Ir direto ao ponto de dor.

## 3. Para quem é

- **Beneficiário direto** — quem usa ou vê a feature (comprador de ingresso? PO/admin do teatro?)
- **Beneficiário indireto** — quem ganha sem interagir diretamente
- Perfil e contexto de uso; em qual momento da jornada a feature entra

## 4. Como melhora a experiência atual

**Antes:** o que o usuário faz hoje, quantas etapas, qual o atrito, qual o pior
momento do fluxo.
**Depois:** o que muda, o que ele para de precisar fazer, o que passa a
acontecer de forma automática ou mais simples.

Se o "depois" não for significativamente melhor que o "antes", a feature precisa
ser repensada.

## 5. Como se conecta com o produto existente

**Dependências obrigatórias:** features/módulos existentes dos quais esta depende.
**O que esta feature habilita no futuro:** o que fica possível depois dela.
**Posição no produto:** core, complementar ou derivada? N1, N2 ou N3?
**RF/RN cobertos:** liste os requisitos funcionais e regras de negócio atendidos.

## 6. O que não é (escopo negativo)

Cada item começa com **"Não é"** ou **"Não inclui"** + justificativa breve. Pelo
menos um item relevante. Se não houver nada fora do escopo, a feature está com
escopo indefinido — revisar antes de aprovar.

## 7. Custos adicionais

Serviços externos (AbacatePay, e-mail transacional), infraestrutura adicional,
implicações de precificação. Se não houver: **"Nenhum custo externo
identificado."** Nunca deixar em branco.

## 8. Decisões tomadas

| Ponto | Decisão |
|---|---|
| [aspecto] | [decisão + justificativa breve] |

Cresce ao longo das iterações. Quando uma pergunta aberta (seção 9) é respondida,
ela migra pra cá.

## 9. Perguntas abertas

Decisões não resolvidas, informação faltante, incertezas. Se não houver:
**"Nenhuma. Todas as decisões de produto estão fechadas."** Nunca deixar em branco.

---

## Checagem antes de marcar como aprovada

1. Uma pessoa não-técnica entende a feature completamente?
2. O problema é específico o suficiente pra validar com um usuário real?
3. O "depois" é significativamente melhor que o "antes"?
4. O escopo negativo tem ao menos um item relevante?
5. Os custos externos estão identificados ou explicitamente ausentes?
6. As decisões tomadas estão registradas na seção 8?
7. As perguntas abertas estão declaradas honestamente?
