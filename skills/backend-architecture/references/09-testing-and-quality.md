# Testes e Qualidade

Diferente do backend privado anterior que inspirou este, o Ludens **tem testes
obrigatórios no pipeline desde o início**. Fonte: `docs.ludens/backend/testing.md`
e `docs.ludens/team/maintainability.md`.

## Gates de merge (não negociáveis)

- **`pytest -q`** verde.
- **`docker build`** limpo.
- **≥ 1 aprovação** de outro desenvolvedor no PR.
- Integra em `master` sem quebrar o build.

Não há threshold numérico de cobertura — o item de DoD é qualitativo: "testes
relevantes criados/atualizados e passando no pipeline".

## Foco: regra de negócio da camada de domínio

O alvo primário são as **regras de negócio do domínio (DDD)**:

- Reserva e compra; controle de disponibilidade de assento (RN05); cálculo de
  preço (inteira = preço cheio; meia = 50%; **sem exigir número de documento de
  estudante** — RN04); processamento de ordem; reembolso por janela (RN02).

### Como testar cada camada

- **Domínio** — sem DB e sem HTTP. Instancia o aggregate, chama o método, faz
  asserção sobre o estado + os eventos acumulados (`aggregate.dequeue_events()`).
  ```python
  def test_meia_entrada_nao_exige_documento():
      reservation = Reservation.open(buyer_id, session_id, quantity=1, ttl_minutes=15)
      ticket = Ticket.issue(reservation_id=reservation.id, type=TicketType.HALF)
      assert ticket.price == full_price * 0.5
      assert ticket.student_document is None  # RN04
  ```
- **Usecases e repositórios** — Postgres real num container. **SQLAlchemy não é
  mockado.** É onde os testes de concorrência de RN05 vivem (duas
  `open_reservation` concorrentes na última poltrona → uma sucede, a outra recebe
  `DomainError`).

Cada feature traz os próprios casos de teste na sua `quality.md`;
`docs.ludens/backend/testing.md` fixa só a abordagem.

## Script de QA manual pré-entrega

`busca do espetáculo → seleção da sessão e do ingresso → reserva → pagamento →
confirmação`. Casos obrigatórios: preço inteira vs. meia; expiração da reserva
devolve os ingressos (RN03); duas compras concorrentes não excedem a capacidade
(RN05); falha de pagamento libera a reserva (RF04); limite por CPF respeitado
(RN01). Mais um **teste de resiliência** (derrubar gateway/e-mail → catálogo no
ar, reserva liberada — RNF03) e um **teste de restart** com reservas abertas.

## Convenções de código (`docs.ludens/backend/code-style.md`)

- PEP 8; `snake_case` para variáveis/funções, `PascalCase` para classes,
  `snake_case` para módulos/arquivos.
- **Sem formatador/linter automatizado na pipeline.** O estilo de um arquivo já
  escrito (espaçamento, quebra de linha, organização) é respeitado exatamente
  como está — nunca reformatado, reordenado ou "limpo" por iniciativa própria.
- Identificadores de domínio em **inglês** (`Show`, `Session`, `Ticket`,
  `Reservation`, `Order`, `User`); **comentários em português**.
- Responsabilidade única; funções/métodos **≤ ~30 linhas** sem justificativa
  técnica.
- **Nenhum `except`/`catch` vazio** — exceção tratada ou logada.
- Violação de regra de negócio → `DomainError` → status HTTP pela camada de API.
- **Nenhum segredo no VCS** — variável de ambiente, `.env` fora do VCS, só
  `.env.example` com valores em branco/dev.
- Issues, user stories e mensagens de commit em português; nomes de branch em
  inglês. **Conventional Commits**, mensagem imperativa em português.

## O que não fazer

- Não presumir que "a API não quebrou visivelmente" é validação suficiente sem
  ter exercitado o caminho alterado.
- Não deixar uma migration só "testada mentalmente" — rodar `alembic upgrade
  head` contra um banco limpo.
- Não ignorar o teste de concorrência de RN05 porque "o caminho feliz passou".
