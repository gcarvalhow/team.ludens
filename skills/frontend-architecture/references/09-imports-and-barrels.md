# Imports e Barrels

## Barrel é entrega, não dívida

Toda subpasta criada numa feature sai com um `index.js` que expõe a superfície
pública daquela camada. Não é etapa opcional que vira dívida técnica — é parte da
definição de "a feature está criada".

Barrels obrigatórios numa feature completa:

```
src/features/{feature}/schemas/index.js
src/features/{feature}/services/index.js
src/features/{feature}/hooks/queries/index.js
src/features/{feature}/hooks/mutations/index.js
src/features/{feature}/hooks/forms/index.js       ← se a pasta existir
src/features/{feature}/components/ui/index.js      ← se a pasta existir
src/features/{feature}/components/index.js
src/features/{feature}/index.js                    ← API pública da feature
```

O `index.js` da raiz da feature re-exporta dos barrels das subpastas, nunca dos
arquivos individuais:

```js
// ✅ certo
export { useBookingMutations } from './hooks/mutations';
export { SessionDetail } from './components';

// ❌ errado — bypassa o barrel
export { useBookingMutations } from './hooks/mutations/useBookingMutations';
```

## Regra de import

- **Cruzou feature ou camada compartilhada** → usar alias (`@catalog/...`,
  `@/lib/...`).
- **Dentro da mesma feature** → usar o barrel da subpasta (`./hooks/queries`),
  não o caminho do arquivo.
- **Import relativo longo** (`../../../features/...`) é proibido — é sintoma de
  arquitetura ruim.

```js
// ✅
import { API_ENDPOINTS } from '@/routes/endpoints';
import { fetcher } from '@/lib/fetcher';
import { useCatalogQueries } from '@catalog/hooks/queries';

// ❌
import { useCatalogQueries } from '../../../features/catalog/hooks/queries/useCatalogQueries';
```

## Aliases

Definidos em dois lugares que precisam concordar: `vite.config.js`
(`resolve.alias`) e `jsconfig.json` (`compilerOptions.paths`) — o segundo é o que
dá autocomplete no editor. Adicionar um alias novo é mexer nos dois.
