# Formulários — react-hook-form + Zod

Formulário no `web.ludens` é a composição de: schema de **request**,
`react-hook-form`, design system (shadcn/ui), mutation de submit, e sincronização
de defaults/edição/reset.

Separar: contrato do dado · lógica de formulário · UI visual do formulário ·
orchestration da tela/dialog/sheet que usa o formulário.

## Stack padrão

`react-hook-form` · `@hookform/resolvers/zod` · schema Zod de **request** ·
componentes de formulário do shadcn/ui.

**O schema do form é o de request, nunca o de response.**

## Estrutura

```
schemas/register.schema.ts          ← payload
server/types/auth.types.ts          ← RegisterDTO = z.infer<...>
hooks/forms/useRegisterForm.ts      ← useForm, defaults, submit, edição
components/forms/RegisterForm.tsx    ← campos, ligação form.control, erros, estado de submit
components/RegisterDialog.tsx        ← abertura/fechamento, contexto da tela
```

## `hooks/forms/`

Quando o formulário passa do trivial, a lógica sobe:

```ts
'use client';

import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { registerSchemaDTO } from '@account/schemas';
import { useAuthMutations } from '@account/hooks/mutations';
import type { RegisterDTO } from '@account/server/types';

export function useRegisterForm({ onSuccess }: { onSuccess?: () => void }) {
  const { register: registerMutation } = useAuthMutations();

  const form = useForm<RegisterDTO>({
    resolver: zodResolver(registerSchemaDTO),
    mode: 'onSubmit',
    defaultValues: { name: '', cpf: '', email: '', password: '' },
  });

  const handleSubmit = form.handleSubmit(async (data) => {
    await registerMutation.mutateAsync(data);
    onSuccess?.();
  });

  return { form, handleSubmit, isPending: registerMutation.isPending };
}
```

Se o form cresce, reaparece em mais de um componente, tem lógica de edição, faz
transformação relevante ou depende de mutation → sai do componente e vai para
`hooks/forms/`.

## Formulário visual (`components/forms/`)

`'use client'`. Foca em layout dos campos, ligação `form.control` ↔ shadcn/ui,
exibição de erros (`<FormMessage />`), estado visual de submit. Recebe `form`,
`onSubmit`, `isPending`. **Não** é dono de mutation, fetch, regra de submit maior
que montar o HTML, nem decisão de fechar dialog.

## `defaultValues`

Sempre explícitos (string → `''`; array → `[]`). Em edição assíncrona, usar
`form.reset({...})` no `useEffect` quando os dados chegam — sincroniza o estado
inteiro e limpa dirty state coerentemente. Não fazer `setValue` campo por campo
sem necessidade.

## Máscaras

CPF/telefone são de exibição. O valor enviado é limpo (só dígitos) — o transform
fica no `onSubmit` ou na service, não espalhado pelos componentes.

## Validação de forma vs. de servidor

- **Forma** (no schema/resolver): formato de CPF (RF09), quantidade 1–6 (RN01
  como limite de forma; o teto real é do backend), e-mail.
- **Servidor** ("CPF já cadastrado", "sessão esgotada"): não entra no resolver —
  vem como erro da mutation e é exibido no campo/toast.

## Anti-padrões

- `useForm()` dentro de `components/ui/`;
- chamar mutation no form visual;
- schema de response validando submit;
- form sem `defaultValues`;
- dialog + mutation + lógica de sucesso + UI do form no mesmo arquivo.
