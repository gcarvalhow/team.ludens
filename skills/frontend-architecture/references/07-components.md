# Componentes

Duas camadas, contrato rígido.

## `components/` — orchestration

Conecta hooks e UI. **Pode**: usar hooks da feature, usar o router, usar context,
montar loading/error/empty state, traduzir contrato técnico em props visuais.
**Não pode**: chamar service direto como atalho; virar componente visual inchado
quando a UI deveria estar em `components/ui`; concentrar orchestration enorme sem
extrair um hook dedicado.

```jsx
// catalog/components/SessionDetail.jsx
import { useCatalogQueries } from '@catalog/hooks/queries';
import { SessionDetailView } from '@catalog/components/ui';

export function SessionDetail({ sessionId }) {
  const { useSessionDetail } = useCatalogQueries();
  const { data, isLoading, isError } = useSessionDetail(sessionId);

  if (isLoading) return <SessionDetailView.Skeleton />;
  if (isError) return <SessionDetailView.Error />;
  if (!data) return <SessionDetailView.Empty />;

  return <SessionDetailView session={data} />;
}
```

## `components/ui/` — apresentação pura

**Pode**: layout, texto, composição visual, estado visual local (hover, aberto,
expandir/colapsar), callbacks recebidos por props. **Não pode**: `useQuery`,
`useMutation`, chamada de service, toast de regra de negócio, handler com
validação de domínio + mutation, fetch para "carregar" o componente.

Se um componente em `components/ui/` precisa saber se há ingresso disponível, ele
recebe isso por prop — não busca.

## Estados assíncronos — sempre os três

Todo componente que consome uma query trata **loading**, **error** e **empty**
explicitamente. Nada de tela em branco enquanto carrega, nada de crash em erro,
nada de lista vazia sem mensagem. É regra de UX (RNF04) e de arquitetura ao mesmo
tempo — ver `references/11`.

## Contagem regressiva da reserva

Onde o fluxo tem uma reserva ativa (`/checkout/:reservationId`), o componente de
orchestration mantém e exibe **o tempo restante até `expiresAt`** de forma
visível e honesta. Quando zera, leva a pessoa a um estado claro ("a reserva
expirou, os ingressos voltaram para a sessão") — não um erro genérico. RN03.
