# Mutations — TanStack Query v5

Toda escrita passa por mutation hook da feature: create, update, cancel, reserve,
pay, resend, etc. A mutation não só chama a API — ela centraliza a estratégia de
cache, a UI otimista quando fizer sentido, o rollback, o tratamento de erro e as
mensagens de sucesso/falha.

## Regra fundamental

Mutation vive em `hooks/mutations/`. O componente pode chamar o hook, decidir
quando executar e reagir ao estado (`isPending`, `isSuccess`, `isError`) — mas
não é onde a regra da mutation é implementada.

## Estrutura

```ts
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { toast } from 'sonner';
import { openReservation } from '@booking/server/services';
import { sessionQueryKeys } from '@catalog/hooks/queries';
import { messageFor } from '@web/lib/api-error';
import type { OpenReservationDTO } from '@booking/server/types';

export function useReservationMutations() {
  const queryClient = useQueryClient();

  const open = useMutation({
    mutationFn: (data: OpenReservationDTO) => openReservation(data),
    onSuccess: (reservation) => {
      void queryClient.invalidateQueries({ queryKey: sessionQueryKeys.detail(reservation.sessionId) });
      toast.success('Ingressos reservados. Você tem 15 minutos para pagar.');
    },
    onError: (error) => {
      toast.error(messageFor(error, {
        seats_unavailable: 'Não há mais ingressos disponíveis para esta sessão.',
        cpf_limit: 'Você já atingiu o limite de 6 ingressos por sessão.',
      }));
    },
  });

  return { open };
}
```

## Shape dos parâmetros

- só payload: `mutationFn: (data: OpenReservationDTO) => openReservation(data)`
- `id` + payload: `mutationFn: ({ id, data }: { id: string; data: UpdateSessionDTO }) => updateSession(id, data)`

Prefira **um único objeto** para operações compostas — evita ordem posicional
frágil.

## `invalidateQueries` vs `refetchQueries`

- **`invalidateQueries`** é o default — marca como stale, refetch no fluxo natural.
- **`refetchQueries`** quando a UX depende da reconciliação imediata (transição de
  estado sensível, backend que recalcula coleções). Não use por reflexo — é mais
  custoso — nem esconda necessidade real de reconciliação.

## UI otimista

Recomendada quando o resultado é previsível, a latência degrada a experiência e o
rollback é razoável. Contrato mínimo: `cancelQueries` → snapshot → update otimista
→ rollback em `onError` → reconciliar em `onSettled`.

**Nunca em disponibilidade de assento** — a verdade de "tem lugar?" é do servidor
(RN05). Mostrar otimisticamente "reservado" e depois falhar destrói a confiança.
Otimista serve para coisas locais (marcar um filtro, expandir um card).

## `mutate` vs `mutateAsync`

- `mutate` — dispara e segue.
- `mutateAsync` — quando o componente precisa coordenar (fechar dialog, navegar,
  resetar form, encadear). Não use `try/catch` redundante se a mutation já
  centraliza o feedback de erro.

## Tratamento de erro

Todo `onError` tem mensagem de toast clara em pt-BR. Nunca silenciar, nunca
`onError` vazio, nunca delegar tudo ao componente. Se a feature tem normalizador
de erro da API (`messageFor`), a mutation usa.

Erro de pagamento / reserva expirada não é toast solto: leva a pessoa de volta a
um estado claro (reserva liberada, pode tentar de novo — RF04).

## Toasts

Pertencem à mutation ou à orchestration acima dela — nunca ao service, nunca a
`components/ui/`. Curtos, pt-BR, específicos, sem jargão técnico.

## Mutations encadeadas

Se a ação envolve mais de uma mutation, a orchestration sobe para
`hooks/components/` ou um hook especializado — não para o componente visual.

## Proibido

- chamar service de `components/ui/`;
- mutation inline no componente;
- mutation sem política clara de cache;
- erro sem feedback;
- UI otimista sem rollback;
- toast dentro de service;
- otimismo em disponibilidade de assento.
