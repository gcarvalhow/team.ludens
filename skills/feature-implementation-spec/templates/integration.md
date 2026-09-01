# TEMPLATE — Contrato de Integração backend→frontend (Ludens)

Modelo canônico do contrato de cada feature. Salvar como
`docs.ludens/specs/[domínio]-[conceito]/integration.md`.

Ciclo de vida:
- Gerado pela skill `feature-implementation-spec` como **contrato-alvo**
  (`status: alvo`) — o frontend constrói contra ele enquanto o backend implementa.
- Atualizado pelo responsável de backend ao fim da implementação para **refletir
  o código real** (`status: canônico`) — cruzando as rotas implementadas com a
  `spec.md` e o `logic.md`.

> Este template é a fonte canônica da estrutura. `docs.ludens/backend/integration/_template.md`
> aponta para cá.

---

## Frontmatter

```yaml
---
status: alvo            # alvo | canônico
spec: [domínio]-[conceito]
updated_at: 2026-09-01
responsavel: Igor (Backend)
---
```

## 1. Identificação e status da feature

Nome; módulo backend responsável; `status` (alvo/canônico/existente); data da
última atualização; responsável técnico.

## 2. Objetivo de negócio

O que a feature entrega, em uma frase, ligada ao RF.

## 3. Escopo atual vs. futuro

O que este contrato cobre agora; o que fica para depois.

## 4. Semântica de produto

O significado dos conceitos que aparecem nas rotas (o que é uma "reserva", uma
"ordem", um "ingresso" nesta feature), em linguagem de produto.

## 5. Dependências

Outras features/módulos, serviços externos (AbacatePay, e-mail), variáveis de
ambiente.

## 6. Rotas públicas

Para cada rota: método, caminho (`<prefixo a definir>/...`), auth exigida
(`get_current_buyer` / `require_admin` / pública), status de sucesso.

## 7. Contrato de request + transforms obrigatórios no frontend

Corpo aceito por rota; validações de forma; transformações que o frontend precisa
aplicar antes de enviar (ex.: CPF sem máscara).

## 8. Contrato de response

Shape por rota; formato canônico vs. de exibição; nulabilidade de cada campo.

## 9. Estados de negócio e transições

Máquina de estados dos conceitos da feature; ordenações e filtros suportados.

## 10. Erros esperados e casos de borda

Em linguagem de negócio: quando cada 4xx acontece, com a mensagem. Envelope de
erro: `<preencher forma exata — a definir globalmente>`.

## 11. Semântica de autenticação / autorização

Quem pode chamar o quê; o que acontece com token expirado / `security_stamp`
regenerado.

## 12. Impacto de UX

O que o frontend precisa mostrar em cada estado (loading / erro / vazio /
sucesso); contadores regressivos (RN03); estados de "pagamento em processamento".

## 13. Frescor de dados, ids estáveis, evolução de contrato

O que pode estar defasado (disponibilidade é quase-tempo-real, ~2s de latência do
relay); quais ids são estáveis; como o contrato evolui sem quebrar o frontend.

## 14. Observabilidade

`traceId` / correlação, se houver.

## 15. Exemplos de payload reais

Request e response reais, por rota.

## 16. Lacunas e decisões em aberto

Convenções ainda não definidas globalmente: prefixo de rota / base path
`<preencher>`; versionamento de API `<preencher>`; forma exata do corpo de erro
`<preencher>`. Divergências entre o que foi especificado e o que foi implementado.
