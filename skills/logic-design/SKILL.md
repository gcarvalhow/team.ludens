---
name: logic-design
description: >
  Skill de lógica de negócio para o Ludens. Complementa a feature-design com
  fluxos por perfil de usuário, estados e transições, regras de negócio e pontos
  de integração entre frontend e backend. Invocada após aprovação da spec de
  produto pelo PO. Produz o contrato compartilhado que permite FE e BE
  trabalharem em paralelo.
user-invocable: true
argument-hint: "[domínio]-[conceito] (ex: booking-reservation)"
---

# Logic Design

A spec de produto define o quê e o porquê. Esta skill define o como — em
linguagem de negócio, não de engenharia.

Antes de uma única linha de código, esta skill responde à pergunta que mais
importa para a engenharia: **como exatamente esta feature se comporta para cada
perfil de usuário, em cada estado, seguindo cada regra?**

---

## Leitura obrigatória antes de pensar

1. `docs.ludens/specs/[domínio]-[conceito]/spec.md` — a spec aprovada (passada como argumento)
2. `docs.ludens/requirements/business-rules.md` — RN01–RN05
3. `docs.ludens/requirements/functional.md` — o RF correspondente (critérios de aceite, dependências)
4. `docs.ludens/backend/integration/_template.md` — a estrutura do contrato backend→frontend que o `integration.md` vai preencher depois

Não prossiga sem ler a spec e as RN.

---

## O que esta skill faz

Produz um documento de lógica de negócio para uma feature já especificada e
aprovada. Não produz contratos de API, schemas, decisões de arquitetura ou
nomenclatura técnica de domínio (Aggregate, Entity, Repository, Value Object).

O output fala em linguagem de produto e de comportamento — estados que o usuário
reconhece, regras que um comprador ou o admin do teatro entenderia.

---

## Processo de pensamento (interno, antes de escrever)

**1. Quais perfis tocam esta feature?**
Os perfis do Ludens são `Comprador` (buyer autenticado) e `Admin` (PO/teatro).
Alguns fluxos também têm o perfil `Visitante` (não autenticado — navega o
catálogo). Para cada um: o que pode iniciar? O que vê? O que não pode fazer? Se
um perfil não interage, declare explicitamente.

**2. Qual é a sequência de estados?**
Para cada conceito principal (reserva, ordem, ingresso, sessão…): quais estados
existem em linguagem de produto? O que causa cada transição (ação do usuário,
evento do sistema, tempo)? O que a bloqueia? Estado é algo que o usuário
reconhece — não um valor de enum.

**3. Quais regras de negócio são inegociáveis?**
Pré-condições para cada ação. Invariantes que nunca podem ser quebradas
(RN05: duas compras concorrentes nunca excedem a capacidade). Limites e tetos
(RN01: 6 ingressos por CPF por sessão). Janelas de tempo (RN02 reembolso, RN03
expiração de 15 min).

**4. O que FE e BE precisam acordar antes de construir?**
Quais dados o frontend precisa conhecer para construir cada estado visual. O que
o backend precisa garantir para o frontend funcionar. Não contratos de API — mas
acordos sobre o que cada lado produz e consome, para os dois construírem em
paralelo.

**5. O que o fluxo principal não cobre?**
Situações não-óbvias quando estados, perfis e regras se combinam de formas
inesperadas. Cada uma com decisão fechada ou marcada como pergunta aberta.

---

## Formato do output

Salvar em `docs.ludens/specs/[domínio]-[conceito]/logic.md` (mesmo
`[domínio]-[conceito]` da spec).

### Frontmatter obrigatório

```yaml
---
status: draft
spec: [domínio]-[conceito]
created_at: 2026-09-01
---
```

Nunca marcar como `reviewed` sem confirmação explícita de revisão conjunta pelos
tech leads de frontend e backend. Após revisão, mudar `status` para `reviewed` e
adicionar `reviewed_at`.

### Seções

1. **Fluxo por perfil** — para cada perfil que interage: prosa curta + lista de
   passos (o que faz, o que vê, o que acontece; o que acontece quando tenta uma
   ação proibida). Sem tabela nesta seção.
2. **Estados e transições** — para cada conceito principal: estados em linguagem
   de produto, o que causa cada transição, o que bloqueia. Sem nomenclatura
   técnica de domínio.
3. **Regras de negócio** — lista objetiva, uma regra por linha. Formato:
   `- [condição/contexto] → [consequência/restrição]`. Referencie a RN.
4. **Pontos de integração** — dois blocos fixos:
   ```
   Frontend precisa saber:
     - [dado, estado ou comportamento que o backend precisa expor]
   Backend precisa garantir:
     - [comportamento, dado ou invariante que o frontend depende]
   ```
   Sem endpoints, sem schemas.
5. **Casos de borda** — cada um com nome, descrição da situação, e decisão
   fechada OU `[pergunta aberta]` com o que precisa ser decidido.

---

## Proibições absolutas

Nunca no output: nomenclatura de domínio técnico (Aggregate, Entity, Repository,
Value Object, Enum); contratos de API, endpoints, métodos HTTP; schemas de banco;
decisões de arquitetura; código; stack; nomes de componentes ou caminhos de
arquivo; cronogramas ou atribuições de sprint.

---

## Checagem final antes de salvar

1. Todos os perfis relevantes têm fluxo completo descrito?
2. Cada ação proibida tem comportamento do sistema descrito?
3. Os estados usam linguagem de produto?
4. Os pontos de integração permitem FE e BE construírem em paralelo?
5. Nenhuma regra de negócio está implícita?
6. Os casos de borda não-óbvios estão nomeados com decisão ou pergunta aberta?

## Quem revisa

O `logic.md` é revisado conjuntamente pelos tech leads de frontend e backend —
não pelo time de produto. A revisão valida que o contrato é implementável e
suficiente para os dois lados trabalharem em paralelo. É o pré-requisito para a
skill `feature-implementation-spec`.
