---
name: api
description: API REST que expõe o agente de moderação.
targets:
  - /2-2_Israel/codigo/api/app.py
  - /2-2_Israel/codigo/api/rotas.py
---

# API do Agente de Moderação

## Tecnologia

- **FastAPI:** Framework para construção da API REST.

## Estrutura

### 1. Rotas e Controladores

> Arquivo: `/2-2_Israel/codigo/api/rotas.py`

Este arquivo deve conter exclusivamente a classe `ControladorModeracao` da API.

A classe deve:

- Receber uma instância da classe `AgenteClassificador` e da classe `GerenciadorBancoDados`.
- Configurar um `APIRouter` do FastAPI.
- Retornar a instância do roteador contendo as rotas registradas, por meio do método `obter_roteador(self) -> APIRouter`.
- Expor o método `moderar(self, comentario: ComentarioEntrada) -> RespostaModeracao`, mapeado para a rota `POST /moderar`.
- Expor o método `listar_historico(self) -> list[ComentarioSaidaBanco]`, mapeado para a rota `GET /historico`.
- Validar todas as entradas e saídas utilizando exclusivamente os esquemas definidos em `esquemas.spec.md`. Não é permitido criar ou modificar esquemas de resposta.

### 2. Inicialização da Aplicação

> Arquivo: `/2-2_Israel/codigo/api/app.py`

Este arquivo deve conter exclusivamente a classe `AgenteModeracaoAPI` da API.

A classe deve:

- Utilizar o padrão *Application Factory* (Fábrica de Aplicação).
- Instanciar a classe `AgenteClassificador` (especificada em `agente_classificador.spec.md`).
- Instanciar a classe `GerenciadorBancoDados` (especificada em `banco.spec.md`).
- Instanciar o `ControladorModeracao`, passando as instâncias do `AgenteClassificador` e do `GerenciadorBancoDados`.
- Configurar as rotas por meio do método `_configurar_rotas(self)`.
- Exportar a variável `app` para o Uvicorn utilizando o método `obter_app(self) -> FastAPI`.

## Endpoints

- `POST /moderar`
  - Body:
    ```json
    {
      "texto": "string"
    }
    ```

  - Response: 
    ```json
    {
      "eh_ofensivo": true | false,
      "nivel_da_ofensa": "nenhuma | levemente | moderadamente | altamente",
      "eh_discurso_de_odio": true | false,
      "justificativa": "string",
      "acao": "Aprovar | Sinalizar | Bloquear",
      "modelo_de_llm": "string | null",
      "provedor_llm": "string | null"
    }
    ```

- `GET /historico`

Retorna a lista dos comentários previamente analisados, ordenados do mais recente para o mais antigo.

  - Response:
    ```json
    [
      {
        "id": 1,
        "texto": "Comentário analisado",
        "eh_ofensivo": true | false,
        "nivel_da_ofensa": "nenhuma | levemente | moderadamente | altamente",
        "eh_discurso_de_odio": true | false,
        "justificativa": "string",
        "acao": "Aprovar | Sinalizar | Bloquear",
        "modelo_de_llm": "string | null",
        "provedor_llm": "string | null",
        "criado_em": "Data (ex.: 2026-07-13T18:25:31)"
      }
    ]
    ```

A resposta deve utilizar exclusivamente o esquema `ComentarioSaidaBanco` definido em `esquemas.spec.md`. Não é permitido criar um esquema específico para este endpoint.

[@test]: /2-2_Israel/testes/teste_api.py#L1-L40