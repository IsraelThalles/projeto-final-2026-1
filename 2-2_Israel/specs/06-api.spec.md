---
name: api
description: API REST que expõe o agente de moderação.
targets:
  - /2-2_Israel/codigo/api/app.py
  - /2-2_Israel/codigo/api/rotas.py
  - /2-2_Israel/codigo/esquemas/esquemas.py
---

# API do Agente de Moderação

## Tecnologia

- **FastAPI:** Framework para construção da API REST.
- **Pydantic:** Para validação de payloads e respostas.

## Contratos de Dados (Centralizados)

Todos os modelos Pydantic do sistema (entrada e saída) devem ser definidos exclusivamente no arquivo `/2-2_Israel/codigo/esquemas/esquemas.py`. O restante do sistema (incluindo o banco de dados) deve importar os contratos deste arquivo.

## Endpoints

- `POST /moderar`
  - Body: `{ "text": string }`
  - Response: 
    ```json
    {
      "eh_ofensivo": boolean,
      "nivel_da_ofensa": "nenhuma | levemente | moderadamente | altamente",
      "eh_discurso_de_odio": boolean,
      "justificativa": "string",
      "acao": "Aprovar | Sinalizar | Bloquear"
    }
    ```

[@test]: /2-2_Israel/testes/teste_api.py#L1-L40