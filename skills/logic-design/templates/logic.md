# TEMPLATE — Logic Doc (Ludens)

Modelo canônico para docs de lógica de negócio do Ludens. Salvar como
`docs.ludens/specs/[domínio]-[conceito]/logic.md`.

> Ler antes: a `spec.md` aprovada da feature; `docs.ludens/requirements/business-rules.md`;
> o RF correspondente em `docs.ludens/requirements/functional.md`.

---

## Por que este documento existe

A spec define o quê e o porquê. O logic doc define o como — em linguagem de
negócio, não de engenharia. Sem ele, frontend e backend interpretam a spec de
formas diferentes e esperam que o outro resolva as ambiguidades durante a
implementação. Um logic doc bem escrito elimina esse atrito na origem: FE e BE
constroem em paralelo porque o contrato entre eles está explícito antes de
qualquer linha de código.

## O que um logic doc não é

- Não é um contrato de API
- Não é um schema de banco
- Não é uma decisão de arquitetura
- Não usa nomenclatura de domínio técnico (Aggregate, Entity, Value Object, Enum, Repository)
- Não é um plano de implementação

---

## Frontmatter obrigatório

```yaml
---
status: draft
spec: [domínio]-[conceito]
created_at: 2026-09-01
---
```

`reviewed` + `reviewed_at` só após revisão conjunta explícita dos tech leads de
FE e BE.

## Cabeçalho

```
# [Nome da feature] — Lógica de Negócio
```

---

## 1. Fluxo por perfil

Para cada perfil que toca a feature (`Visitante`, `Comprador`, `Admin`): fluxo
completo do ponto de vista dele.

- O que ele pode iniciar
- Cada passo: o que faz, o que vê, o que acontece como resultado
- O que acontece quando tenta uma ação proibida para ele

Prosa curta + lista de passos. Sem tabela. Cobrir apenas perfis que efetivamente
interagem.

## 2. Estados e transições

Para cada conceito principal da feature:
- Quais estados existem (linguagem de produto)
- O que causa cada transição (ação do usuário, evento do sistema, tempo)
- O que bloqueia cada transição

Sem nomenclatura técnica de domínio. Use o nome que o usuário usaria.

## 3. Regras de negócio

Lista objetiva, uma regra por linha:
`- [condição ou contexto] → [consequência ou restrição] (RNxx)`

Cobre pré-condições, invariantes, limites e janelas de tempo. Referencie a RN
sempre que aplicável.

## 4. Pontos de integração

```
Frontend precisa saber:
  - [dado, estado ou comportamento que o backend precisa expor]

Backend precisa garantir:
  - [comportamento, dado ou invariante que o frontend depende]
```

Sem contratos de API. Sem endpoints. Sem schemas.

## 5. Casos de borda

Cada um com:
- Nome do caso
- Descrição da situação
- Decisão fechada OU `[pergunta aberta]` com o que precisa ser decidido

---

## Checagem final antes de salvar

1. Todos os perfis relevantes têm fluxo completo?
2. Cada ação proibida tem comportamento do sistema descrito?
3. Os estados usam linguagem de produto?
4. Os pontos de integração permitem FE e BE construírem em paralelo?
5. Nenhuma regra de negócio está implícita?
6. Os casos de borda não-óbvios estão nomeados com decisão ou pergunta aberta?

## Quem revisa

Tech leads de frontend e backend, em conjunto. Após revisão: `status: reviewed` +
`reviewed_at`. É o pré-requisito para `feature-implementation-spec`.
