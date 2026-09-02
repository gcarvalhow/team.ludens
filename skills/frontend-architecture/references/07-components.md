# Componentes — Separação entre UI e Orchestration

Regra mais importante do frontend: **componente visual não é lugar de regra de
negócio.** As camadas de componente são separadas para a UI não virar o centro
de mutation, query, navegação contextual, validação de domínio ou fluxos
assíncronos complexos.

## As camadas

1. **`components/ui/`** — visual puro (da feature; o shadcn/ui fica em `src/components/ui/`).
2. **`components/forms/`** — visual de formulário da feature.
3. **`components/`** — composição e orchestration entre hooks, contexts e UI.
4. **`hooks/components/`** — apoio, quando a orchestration de um componente cresceu demais.

## `components/ui/`

**Pode**: `'use client'`; `useState`/`useEffect`/`useMemo` para estado visual
local; hover, expand/collapse, tab/accordion visual; callbacks recebidos por
props; renderização condicional por props; markup, classes e variants do design
system.

```tsx
'use client';

interface SessionCardProps {
  title: string;
  statusLabel: string;
  availableLabel: string;
  onSelect: () => void;
}

export function SessionCard({ title, statusLabel, availableLabel, onSelect }: SessionCardProps) {
  const [hovered, setHovered] = useState(false);
  return (
    <Card onMouseEnter={() => setHovered(true)} onMouseLeave={() => setHovered(false)}>
      <CardHeader>
        <span>{title}</span>
        <Badge>{statusLabel}</Badge>
      </CardHeader>
      {hovered ? (
        <CardFooter>
          <span>{availableLabel}</span>
          <Button onClick={onSelect}>Reservar</Button>
        </CardFooter>
      ) : null}
    </Card>
  );
}
```

**Proibido**: `useQuery`, `useMutation`, service call, `fetcher`, toast de regra
de negócio, handler que valida regra de domínio e faz `mutateAsync`, receber só
um `id` e buscar dado internamente, decidir cancelar/arquivar/deletar por conta
própria.

## `components/`

Liga query hooks, mutation hooks, `hooks/forms`, `hooks/components`, contexts,
router (`next/navigation`) e a UI. Pode consumir hooks, preparar props derivadas,
converter contrato bruto em contrato visual, coordenar abertura/fechamento,
acionar navegação, tratar loading/empty/error.

```tsx
'use client';

import { useCatalogQueries } from '@catalog/hooks/queries';
import { SessionDetailView } from '@catalog/components/ui';

export function SessionDetail({ sessionId }: { sessionId: string }) {
  const { useSessionDetail } = useCatalogQueries();
  const { data, isLoading, isError } = useSessionDetail(sessionId);

  if (isLoading) return <SessionDetailView.Skeleton />;
  if (isError) return <SessionDetailView.Error />;
  if (!data) return <SessionDetailView.Empty />;

  return <SessionDetailView session={data} />;
}
```

Evitar virar monólito de 500 linhas — extrair orchestration para `hooks/components/`.

## `hooks/components/`

Lugar da orchestration quando o componente coordena muitas mutations, tem lógica
de confirm/cancel/retry complexa, muitos handlers, ou muito estado local
misturado com estado de servidor. Handler com validação de negócio + mutation +
side effect de navegação/fechamento é orchestration e **sai** do `components/ui/`.

## Regras de props

UI recebe: dado pronto, labels prontas, callbacks prontos, flags de
loading/pending. **Evitar** passar: `id` cru que a UI não precisa; objeto de
mutation; query result inteiro; `queryClient` ou service.

## Loading, error e empty

Vivem em `components/` (dependem da leitura do servidor). `components/ui/` recebe
skeletons/placeholders, mas não é dono do fetch que decide qual estado mostrar.
Distinguir loading de vazio — nunca mostrar empty enquanto carrega.

## Contagem regressiva da reserva

Onde o fluxo tem uma reserva ativa (`/checkout/[reservationId]`), o componente de
orchestration mantém e exibe **o tempo restante até `expiresAt`** de forma
visível e honesta. Ao zerar, revalida o estado com a API e leva a pessoa a um
estado claro ("a reserva expirou, os ingressos voltaram para a sessão") — nunca
um erro genérico. RN03.

## Anti-padrões

- `components/ui` importando hook de mutation ou service;
- componente visual buscando dado por id;
- `components/forms` virando lugar de mutation;
- `components/` acumulando tudo sem extrair `hooks/components`;
- props recebendo o Query result completo quando 3 campos bastariam.
