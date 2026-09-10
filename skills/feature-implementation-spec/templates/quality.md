# TEMPLATE — `quality.md` (Ludens)

Toda a estratégia de teste de uma feature: Definition of Ready, casos de domínio
(pytest) com código pronto, testes de integração cross-surface, roteiro manual e
riscos. Salvar como `docs.ludens/specs/[domínio]-[conceito]/quality.md`.

> Pré-condição: `spec.md` (`approved`) e `logic.md` (`reviewed`) da mesma feature.
> Regra de ouro: os casos de domínio vêm com o **código completo do arquivo de
> teste**, não com uma descrição de cenário.

---

## Frontmatter

```yaml
---
status: draft
spec: [domínio]-[conceito]
surface: quality
created_at: AAAA-MM-DD
---
```

## Cabeçalho (igual nos três documentos)

```
# [Nome da feature] — Quality
```

**Resumo:** 2–3 linhas do que a feature entrega, ponta a ponta.
**RF:** RFxx · **RN:** RNxx, RNyy · **Módulo backend:** `booking`
**Contrato:** `docs.ludens/specs/[domínio]-[conceito]/integration.md`

---

## 1. Definition of Ready — checagem

Item a item de `docs.ludens/team/quality.md`. Marcar ✅ / ❌ e apontar o que falta.

| Item DoR | Situação |
|---|---|
| Critérios de aceite testáveis | |
| Contrato (`integration.md`) definido | |
| RN citadas com valores aprovados | |
| Dependências de outras features resolvidas | |

## 2. Casos de teste de domínio (pytest)

Uma linha por caso na tabela, e abaixo **o arquivo de teste completo**.

| Caso | Cenário (estado → ação → asserção) | RN/RF |
|---|---|---|
| `test_...` | ... | RFxx |

```python
# tests/modules/<mod>/test_<x>.py  — novo
import pytest
# ... arquivo completo, sem elipses ...
```

## 3. Testes de integração cross-surface

O fluxo que atravessa backend + frontend, e o que cada verificação cobre.

| Fluxo | Verifica |
|---|---|
| cadastro → login → rota protegida responde | token no header, `security_stamp` válido |
| ... | ... |

## 4. Roteiro de teste manual pré-entrega

`busca do espetáculo → seleção da sessão e do ingresso → reserva → pagamento →
confirmação` + casos obrigatórios da feature (preço inteira/meia; expiração
devolve ingressos; duas compras concorrentes não excedem capacidade; falha de
pagamento libera reserva; limite por CPF) + resiliência (derrubar gateway/e-mail)
+ restart com reservas abertas.

Passo a passo numerado, com o resultado esperado de cada passo.

## 5. Riscos e pontos de atenção

- ...

## 6. Passo a passo TBD (QA)

```
git checkout master && git pull && git checkout -b test/<NN>-<slug>
git add tests/modules/<mod> && git commit -m "test(<mod>): cobrir <regras> de <x>"
```

## 7. Bloqueios em aberto

Liste `[bloqueio: decidir antes de implementar]` herdado de `spec.md`/`logic.md`.
