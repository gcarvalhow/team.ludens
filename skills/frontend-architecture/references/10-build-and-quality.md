# Build e Qualidade de Código

Qualidade no `web.ludens` significa código que compila, respeita o lint, está
formatado, passa nos testes cabíveis e não esconde inconsistência estrutural.
Build limpo é parte da definição de pronto.

## Comandos do projeto

```bash
npm run build     # next build — inclui type check do TypeScript
npm run lint      # eslint (config next)
npm run format    # prettier
npm run test      # testes (ver references/13)
npx playwright test
```

## Ordem de validação

1. `npm run build`
2. `npm run lint`
3. `npm run test`
4. `npx playwright test` quando a mudança afeta UI ou fluxo
5. `npm run format` antes do fechamento, se necessário

## O que `npm run build` valida

Build do Next + type checking do TypeScript + imports inexistentes + erros de App
Router + uso incorreto de Server/Client Components + inconsistências que só
aparecem em produção.

Implicações: `noUnusedLocals` quebra; alias errado quebra; componente com hook
sem `'use client'` quebra; assinatura errada de rota App Router quebra.

## O que `npm run lint` valida

ESLint com regras base de JS, `typescript-eslint`, `eslint-plugin-react`, regras
do Next, `react-hooks/recommended`. Warning tolerado pelo tooling não é convite
para degradar o código.

## Portões de merge

CI em `push`/PR para `master`: `npm run build` verde · `npm run lint` verde ·
**1 aprovação** de outro desenvolvedor · integra em `master` sem quebrar o build.

## O que não pode entrar no código final

- `console.log` de debug esquecido;
- import não usado;
- arquivo morto desconectado da feature;
- contrato quebrado escondido por `as`/cast desnecessário;
- código novo copiando padrão ruim do legado sem justificativa;
- componente visual com orchestration indevida;
- subpasta sem barrel.

## Como reportar

Dizer quais comandos foram rodados, o que passou, o que falhou, se a falha é
pré-existente ou introduzida, e se algum passo não se aplicava ao escopo. Nunca
"não testei" sem explicação.
