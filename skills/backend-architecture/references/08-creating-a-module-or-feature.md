# Como Criar um Módulo Novo ou Estender um Existente

Existem 5 módulos (`identity`, `catalog`, `booking`, `payment`, `notification`).
Na prática **estender um módulo existente é o caso comum** — criar um módulo do
zero é raro. Os dois casos seguem a mesma ordem de camadas.

O ADR `docs.ludens/backend/design/002-monolito-modular.md` fixa: só a **base**
(padrões comuns + lista de módulos) é definida antes do código. Cada feature
entra **por spec, uma de cada vez** (`docs.ludens/specs/[domínio]-[conceito]/`), e
a doc é atualizada junto com o código.

---

## Quando criar um módulo novo vs. estender

Criar módulo novo só quando o domínio novo tem identidade própria e não cabe como
método novo em `Show`, `Session`, `Reservation`, `Order`, `Ticket` ou `Buyer` sem
violar o invariante deles. Antes de criar, pergunte: isso é um aggregate novo, ou
é `Session` ganhando mais um método?

---

## Sequência obrigatória

### 1. Domínio primeiro

`domain/aggregates/<nome>.py` (ou `entities/` se for filha). Definir: os campos e
o invariante que protegem; os métodos que mudam estado (**nunca atribuição direta
de campo por fora**); os eventos que cada método levanta, em `domain/events/`.

`raise_event` (de `AggregateRoot`) cuida de incrementar a versão, aplicar o
evento no próprio estado (`_apply` → `_when_<Evento>`) e enfileirar. O aggregate
nunca seta `self.campo = ...` direto — só o handler `_when_*`.

### 2. Repositório

`infrastructure/repositories/<nome>_repository.py`, estendendo
`AggregateRepository[T]` (se levanta evento) ou `BaseRepository[T]` (se é filha).
Só adicionar método se a query for específica (agregação, `JOIN`, `COUNT`
condicional). As contagens que sustentam RN01/RN05 são exemplo legítimo.

### 3. Schemas

`application/schemas/request.py` e `response.py` — Pydantic. Request valida
forma, não regra de negócio. Response nunca expõe o aggregate direto.

### 4. Usecase

`application/usecases/<nome>_usecase.py`. Único lugar que mistura domínio + repo
numa transação. Se precisar de algo de outro módulo, importa de
`dependencies.py` do outro módulo, nunca de `domain/`/`infrastructure/` dele. Se
o fluxo toca disponibilidade de assento, `find_by_id_for_update` na `Session`
antes de qualquer contagem.

### 5. Handler de outbox (se a feature tem efeito externo)

`modules/<mod>/handlers.py`, `@register("EventoX")`, idempotente. Importado no
boot por `main.py`. **Nenhum efeito externo (e-mail, gateway) fora daqui** —
exceção única: criação síncrona da cobrança Pix no checkout.

### 6. Router

`api/routers/<recurso>_router.py`, endpoint chamando o usecase, incluído no
`router.py` do módulo. Escolher a dependency de auth certa (`get_current_buyer`,
`require_admin`, ou nenhuma para catálogo público).

### 7. Módulo consumido por outro? Exportar em `dependencies.py`

Nunca deixar o outro módulo importar `domain/`/`infrastructure/` direto. Se o
retorno é dado, devolver um tipo próprio da fronteira, não o aggregate.

### 8. Migration

`alembic revision --autogenerate` + **revisar o arquivo gerado à mão**
(autogenerate erra rename de coluna, índice parcial). `alembic upgrade head`
antes de testar.

---

## Ordem resumida

```
1. domain/aggregates ou entities (+ domain/events se levanta evento)
2. infrastructure/repositories (estende BaseRepository/AggregateRepository)
3. application/schemas (request/response)
4. application/usecases (domínio + repo numa transação)
5. modules/<mod>/handlers.py (se há efeito externo) — @register, idempotente
6. api/routers (endpoint, incluído no router.py do módulo)
7. dependencies.py — se outro módulo consome isso
8. alembic revision --autogenerate + revisar
```

---

## Checklist antes de considerar a feature pronta

- [ ] O aggregate tem método próprio pra cada mudança de estado — nenhum
      `setattr` direto de fora de `domain/`.
- [ ] Todo evento necessário foi modelado em `domain/events/` e é levantado via
      `raise_event`, nunca construído solto.
- [ ] O repositório novo estende `BaseRepository`/`AggregateRepository` e só
      define método que não existia no core.
- [ ] Nenhum `import` de `domain/`/`infrastructure/` de outro módulo — tudo via
      `dependencies.py`.
- [ ] Nenhum efeito externo (e-mail, gateway) fora de um handler de outbox —
      exceto a criação síncrona da cobrança Pix no checkout.
- [ ] Todo handler de outbox é idempotente.
- [ ] Operação de reserva/confirmação/liberação usa `find_by_id_for_update` na
      `Session` — nunca leitura simples + update (RN05).
- [ ] Meia-entrada: emissão do ingresso **não** exige número de documento de
      estudante (RN04) — e o teste reflete isso.
- [ ] Remoção usa `is_active`/estado de domínio (sessão com venda: cancela, não
      deleta), não `DELETE`.
- [ ] Migration gerada e revisada manualmente.
- [ ] `ruff check .` e `pytest -q` verdes.

Este checklist é o que o `senior-dev` (agent do team.ludens) tende a cobrar em
revisão — rode por ele antes de abrir PR.
