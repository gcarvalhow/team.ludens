# Formulários (react-hook-form + Zod)

## O schema de request guia o form — nunca o de response

```js
// account/hooks/forms/useRegisterForm.js
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { registerSchema } from '@account/schemas';
import { useAccountMutations } from '@account/hooks/mutations';

export function useRegisterForm() {
  const { register: registerMutation } = useAccountMutations();

  const form = useForm({
    resolver: zodResolver(registerSchema),   // schema de REQUEST
    defaultValues: { cpf: '', email: '', password: '' },
  });

  const onSubmit = form.handleSubmit((values) => registerMutation.mutate(values));

  return { form, onSubmit, isPending: registerMutation.isPending };
}
```

## Regras

- `hooks/forms/` **pode**: `useForm`, resolver Zod, integrar com mutations,
  preparar `defaultValues`, sincronizar edição via `reset`.
- **Não pode**: renderizar JSX, fazer fetch direto, acumular lógica que é
  orchestration de tela inteira (isso vai para `components/`).
- Validação de forma no schema: formato de CPF (RF09), quantidade entre 1 e 6
  (RN01 como limite de forma; o teto real é validado no backend), e-mail. Regra
  de servidor ("CPF já cadastrado", "sessão esgotada") **não** entra no resolver
  — vem como erro da mutation e é exibida no campo/toast.
- Máscaras (CPF, telefone) são de exibição — o valor enviado é limpo; o transform
  fica no `onSubmit` ou na service, não espalhado pelos componentes.
- Todo form tem estado de `isPending` desabilitando o submit, e mensagens de erro
  por campo específicas e acionáveis (RNF04).
