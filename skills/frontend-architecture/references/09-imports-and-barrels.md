# Imports e Barrels

Import é parte da arquitetura: define qual camada conhece qual, qual é a API
pública de uma feature e o que é detalhe interno.

Regra central: **todo import interno sai de um `index.ts` público quando esse
barrel já existir.**

## Barrel é entrega, não dívida

Toda subpasta criada numa feature sai com `index.ts` — no momento da criação, não
retroativamente. A feature só está criada quando cada subpasta tem seu barrel.

Barrels obrigatórios:

```
src/features/{feature}/schemas/index.ts
src/features/{feature}/server/services/index.ts
src/features/{feature}/server/types/index.ts
src/features/{feature}/server/index.ts
src/features/{feature}/hooks/queries/index.ts
src/features/{feature}/hooks/mutations/index.ts
src/features/{feature}/hooks/forms/index.ts       ← se a pasta existir
src/features/{feature}/components/forms/index.ts   ← se a pasta existir
src/features/{feature}/components/ui/index.ts      ← se a pasta existir
src/features/{feature}/components/index.ts
src/features/{feature}/index.ts                    ← API pública da feature
```

O `index.ts` da raiz re-exporta dos barrels das subpastas, nunca dos arquivos:

```ts
// ✅ certo
export { useReservationMutations } from './hooks/mutations';
export { SessionDetail } from './components';

// ❌ errado — bypassa o barrel
export { useReservationMutations } from './hooks/mutations/useReservationMutations';
```

## Ordem de preferência dos imports

1. Alias público da feature ou shared layer (`@web/...`, `@catalog/hooks/queries`).
2. Alias de subpasta da própria feature (`@catalog/schemas`) — nunca caminho
   relativo cruzando diretórios.
3. Import relativo apenas no **mesmo diretório** (`./query-options`).
4. Arquivo direto só quando o barrel causaria circular real comprovada.

```ts
// ✅
import { API_ENDPOINTS } from '@web/routes/endpoints';
import { fetcher } from '@web/lib/fetcher';
import { useCatalogQueries } from '@catalog/hooks/queries';

// ❌
import { useCatalogQueries } from '../../../features/catalog/hooks/queries/useCatalogQueries';
```

## Ordem dos blocos de import

1. bibliotecas externas (`react`, `@tanstack/react-query`, `sonner`);
2. Next.js (`next/navigation`, `next/link`);
3. aliases compartilhados (`@web/...`, `@components/ui`);
4. aliases de feature (`@catalog/...`);
5. relativos internos (`./constants`);
6. `import type` seguindo o mesmo agrupamento.

## `import type`

Sempre que o import existir só para tipagem: `import type { Order } from
'@checkout/server/types';`. Evita carga de runtime e deixa explícito o que é valor.

## Direção entre camadas

```
schemas → server/services → server/types → hooks → components → components/ui
```

- `components/ui` não importa `hooks`;
- `server/services` não importa `components`;
- `schemas` não importa `hooks` nem `components`;
- mutation hook pode importar query keys, não componente;
- componente importa hook e UI, não service direto.

## Aliases

Definidos em `tsconfig.json` (`compilerOptions.paths`). O Next resolve a partir
daí. Adicionar um alias novo é mexer só nesse arquivo.

## Anti-padrões

- alias errado para caminho que já tem barrel público;
- misturar barrel e deep import da mesma área no mesmo arquivo;
- importar de arquivo privado quando a pasta já expõe `index`;
- barrel gigante que exporta tudo sem critério;
- caminho relativo longo cruzando feature;
- criar arquivos de uma camada sem criar o barrel na mesma entrega.
