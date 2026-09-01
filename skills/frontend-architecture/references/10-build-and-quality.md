# Build e Qualidade

## Gates de merge (`docs.ludens/backend/testing.md`, seção frontend)

- **`npm run lint`** verde (ESLint + Prettier, obrigatório no pipeline).
- **`npm run build`** verde (Vite build).
- **≥ 1 aprovação** de outro desenvolvedor no PR.
- Integra em `master` sem quebrar o build.

`npm run lint` e `npm run build` **passam antes de qualquer commit** — não deixe
para o CI descobrir.

## Testes

O `web.ludens` hoje não tem testes de componente definidos como gate — o único
gate automatizado é o lint. Testes de componente são **TBD** (documentados como
lacuna em `docs.ludens/backend/testing.md`). Não invente uma suíte que não existe
nem sugira uma stack de teste como se fosse a convenção adotada — se testes de
frontend forem introduzidos, isso é decisão de arquitetura a documentar em
`docs.ludens` antes de virar convenção.

Enquanto isso, a rede de segurança do frontend é: lint verde + build verde + o
roteiro de teste manual pré-entrega do QA (`agents/qa-engineer.md`) + a revisão
do PR.

## Convenções que o lint não pega sozinho

- Nenhum `console.log` deixado no código de produção (só em `onError` de mutation,
  se ajudar debug — e mesmo aí, preferir não).
- Nenhum segredo no código nem no bundle — só `VITE_*` de `.env`, e `.env` fora
  do VCS (só `.env.example`).
- Nenhum dado pessoal (CPF, e-mail, histórico) em `localStorage` direto — usar o
  padrão de auth da feature `account` (RNF01). `localStorage` só para preferência
  de UI não sensível, documentada no código.
- Todo estado assíncrono com loading/error/empty tratados (é regra de UX e de
  arquitetura — `references/07` e `references/11`).

## Passo a passo TBD

```
git checkout master && git pull && git checkout -b feat/<NN>-<slug>
# commits por camada (ver implementation-spec.md da feature)
npm run lint && npm run build      # antes de cada push
/team-ludens:tbd-pr
```
