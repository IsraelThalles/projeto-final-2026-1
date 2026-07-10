---
name: api
description: API REST que expõe o agente de moderação.
targets:
  - /2-2_Israel/codigo/api/app.py
  - /2-2_Israel/codigo/api/rotas.py
---

# API do Agente de Moderação

## Endpoints

- `POST /moderar`
  - Body: `{ "text": string }`
  - Response: 
    ```json
    {
      "eh_ofensivo": boolean,
      "nivel_da_ofensa": "nenhuma | levemente | moderadamente | altamente",
      "eh_discurso_de_odio": boolean,
      "confianca": float,
      "justificativa": "string",
      "acao": "Aprovar | Sinalizar | Bloquear"
    }
    ```

[@test]: /2-2_Israel/testes/teste_api.py#L1-L40