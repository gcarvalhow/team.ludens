# Mutations (TanStack Query v5)

## Toda mutation faz três coisas

1. Invalida (ou atualiza) as queries afetadas.
2. Toast de **sucesso**.
3. Toast de **erro** (mensagem em linguagem de negócio, não técnica — RNF04).

```js
// booking/hooks/mutations/useBookingMutations.js
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { toast } from 'sonner';
import { openReservation, confirmReservation } from '@booking/services';
import { sessionKeys } from '@catalog/hooks/queries';

export function useBookingMutations() {
  const qc = useQueryClient();

  const open = useMutation({
    mutationFn: openReservation,
    onSuccess: (reservation) => {
      qc.invalidateQueries({ queryKey: sessionKeys.detail(reservation.sessionId) });
      toast.success('Ingressos reservados. Você tem 15 minutos para pagar.');
    },
    onError: (error) => {
      toast.error(messageFor(error, {
        seats_unavailable: 'Não há mais ingressos disponíveis para esta sessão.',
        cpf_limit: 'Você já atingiu o limite de 6 ingressos por sessão.',
      }));
    },
  });

  return { open, confirm: /* ... */ };
}
```

## Regras

- `hooks/mutations/` **pode**: `useMutation`, chamar services, invalidar/refetch,
  UI otimista + rollback, toasts.
- **Não pode**: importar componente, conter JSX, viver dentro de `components/ui`,
  substituir `hooks/forms` quando a lógica for claramente de formulário.
- A key de invalidação vem do mesmo builder que a query usou
  (`sessionKeys.detail(id)`), nunca uma string literal.
- **UI otimista** é bem-vinda onde ajuda a sensação de resposta (RNF04), mas
  **nunca em disponibilidade de assento** — a verdade de "tem lugar?" é do
  servidor (RN05); mostrar otimisticamente "reservado" e depois falhar destrói a
  confiança. Otimista serve para coisas locais (marcar um filtro, expandir um
  card), não para o resultado de uma reserva.
- Erro de pagamento / reserva expirada não é toast solto: leva a pessoa de volta
  a um estado claro (reserva liberada, pode tentar de novo — RF04).
