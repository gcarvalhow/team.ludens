---
name: backend-architecture
description: Regras canônicas de arquitetura e código para o backend (api.ludens) do Ludens — DDD, Monólito Modular, Event-Driven via Outbox in-process (sem broker). Carregar antes de qualquer implementação em api.ludens. Contém 10 arquivos de referência cobrindo cada camada, o fluxo de eventos e a fonte de verdade viva em docs.ludens. Escopo é api.ludens — para o frontend use frontend-architecture.
---

# Backend Architecture — DDD, Monólito Modular, Outbox in-process

Esta é a skill mestra de arquitetura e código do backend do Ludens
(`api.ludens`), a plataforma de venda de ingressos do teatro comunitário.

**Ação obrigatória ao carregar esta skill:**

Ler TODOS os arquivos de referência em `skills/backend-architecture/references/`
em ordem numérica. Não pular nenhum arquivo. Não resumir. Ler na íntegra.

---

## Os três padrões que sustentam este backend

### Domain-Driven Design (DDD)

O domínio (regra de negócio) vive isolado de framework, banco e transporte, em
`domain/` dentro de cada módulo. `Show`, `Session`, `Reservation`, `Order`,
`Ticket`, `Buyer` são **aggregate roots** — entidades com identidade própria que
carregam seus invariantes e só mudam de estado pelos próprios métodos
(`Reservation.confirm()`, `Order.refund()`), nunca por atribuição direta de campo
por fora. Detalhe de cada camada em `references/02` a `references/05`.

### Monólito Modular

Um único serviço deployável, internamente dividido em cinco módulos de negócio
isolados — `identity`, `catalog`, `booking`, `payment`, `notification`. Cada
módulo é dono do próprio `domain/`, `infrastructure/`, `application/` e router, e
**nenhum módulo importa o `domain`/`infrastructure` interno de outro
diretamente**. Quando um módulo precisa de algo de outro, o outro **exporta** uma
função de dependência explícita no seu `dependencies.py` (`identity` exporta
`get_current_buyer` / `require_admin`; `catalog` exporta uma referência de sessão
para `booking` ler a capacidade). Regra completa em `references/06`.

### Event-Driven Architecture via Outbox in-process

Um usecase nunca dispara um efeito colateral externo (e-mail de confirmação,
estorno no gateway) diretamente. O efeito vira uma linha `Event`
(`dispatched_at = NULL`) gravada **na mesma transação** que muda o estado de
domínio, via `AggregateRepository.save()`. Um relay em background (`asyncio.Task`
no `lifespan`) faz polling da tabela `events` a cada `OUTBOX_RELAY_INTERVAL_SECONDS`
(padrão 2s) e chama **handlers Python registrados por `event_type`** num registry
in-process — **não há broker, não há RabbitMQ**. Isso troca uma transação
distribuída por uma transação local + entrega *at-least-once* — o preço é que os
handlers precisam ser idempotentes. Mecanismo completo em `references/07`.

> Diferença deliberada em relação a um backend privado anterior do mesmo autor
> (que inspirou este):
> **sem Event Sourcing**, **sem CQRS/read model**, **sem message broker** — o
> relay chama funções Python no mesmo processo. As tabelas de domínio são a
> fonte de verdade; `events` é só a fila de efeitos de saída.

---

## Fonte de verdade viva

Este documento descreve o *padrão* e o *porquê*. Para o que está implementado
**hoje**, a fonte de verdade é `docs.ludens`, mantida por quem muda o código:

- `docs.ludens/backend/overview.md` — documento-mestre (anatomia de módulo,
  skeleton de arquivos, os 5 módulos).
- `docs.ludens/backend/design/00x-*.md` — ADRs (`001` outbox in-process, `002`
  monólito modular), cada um com porquê/consequências e status.
- `docs.ludens/backend/security/authentication.md` — dual-token JWT,
  `security_stamp`, bcrypt.
- `docs.ludens/backend/security/configuration.md` — variáveis de ambiente.
- `docs.ludens/specs/[domínio]-[conceito]/` — spec + logic + integration +
  implementation-spec de cada feature.

Se este documento divergir do que `docs.ludens` ou o código dizem, **o código e
`docs.ludens` vencem** — pare e sinalize. Mapa completo em `references/10`.

---

## Arquivos a carregar (ordem obrigatória)

```
01-project-context.md
02-core-layer.md
03-domain-layer.md
04-application-layer.md
05-infrastructure-layer.md
06-api-layer-and-module-boundaries.md
07-outbox-and-event-flow.md
08-creating-a-module-or-feature.md
09-testing-and-quality.md
10-docs-ludens-map.md
```

---

## Princípios de aplicação

### Toda regra é mandatória

As regras nesses arquivos não são sugestões nem best practices situacionais. São
regras. Não negociáveis — salvo quando `docs.ludens` ou o código já implementado
documentarem explicitamente uma exceção.

### Em caso de conflito entre abordagens

Na dúvida entre duas abordagens válidas, escolher a que respeita mais
estritamente o invariante do domínio.

- Mudar um campo direto vs. criar um método no aggregate → criar o método.
- Chamar o gateway/e-mail direto no usecase vs. gravar um `Event` na mesma
  transação → gravar o `Event`.
- Importar `domain` de outro módulo vs. pedir uma dependência exportada → pedir a
  dependência exportada.
- Reimplementar uma query genérica vs. estender `BaseRepository`/`AggregateRepository`
  → estender.
- Leitura simples + update numa operação de reserva/compra vs.
  `find_by_id_for_update` → `find_by_id_for_update` (RN05).

### Violação detectada → parar e corrigir

1. Parar a task atual. 2. Identificar a regra violada (citar arquivo e seção de
`references/`). 3. Corrigir. 4. Continuar só após a correção. 5. Nunca avançar
com violação conhecida em aberto.

---

## Resumo das regras mais críticas (referência rápida)

| Área | Regra mais crítica |
|------|--------------------|
| Domínio | Aggregate muda de estado só pelos próprios métodos — nunca atribuição direta de campo por fora |
| Application | `usecases/` é o único lugar que mistura domínio + infra numa transação; `schemas/` nunca vaza objeto de domínio pra API |
| Infraestrutura | Repositório de módulo estende `BaseRepository`/`AggregateRepository` — não reimplementa query genérica que já existe em `core/` |
| Módulos | Nenhum módulo importa `domain`/`infrastructure` interno de outro — só dependência exportada em `dependencies.py` |
| Eventos | Efeito colateral externo (e-mail, estorno) vira `Event` na mesma transação — nunca chamada direta ao serviço no usecase |
| Concorrência | Reservar / confirmar / liberar assento usa `find_by_id_for_update` — nunca leitura simples seguida de update (RN05) |
| Soft delete | Remoção é `is_active = False` via método de domínio — nunca `DELETE FROM` |
| Segredo | Nunca no VCS — variável de ambiente, `.env` fora do VCS, só `.env.example` com valores em branco/dev |
| Docs | `docs.ludens` é a fonte viva — esta skill explica o padrão, não substitui checar o estado atual lá |
| Git | Fluxo gerenciado por `/team-ludens:tbd-start`, `/team-ludens:tbd-commit`, `/team-ludens:tbd-pr` |
