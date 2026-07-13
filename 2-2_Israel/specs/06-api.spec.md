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
- Expor o método `moderar(self, comentario: ComentarioEntrada) -> RespostaModeracao` mapeado para a rota `POST`.
- Validar a resposta utilizando os esquemas definidos em `esquemas.spec.md`. Não é permitido criar ou modificar esquemas de resposta.

### 2. Inicialização da Aplicação

> Arquivo: `/2-2_Israel/codigo/api/app.py`

Este arquivo deve conter exclusivamente a classe `AgenteModeracaoAPI` da API.

A classe deve:

- Utilizar o padrão *Application Factory* (Fábrica de Aplicação).
- Instanciar da classe `AgenteClassificador` (especificada em `agente_classificador.spec.md`).
- Instanciar da classe `GerenciadorBancoDados` (especificada em `banco.spec.md`).
- Instanciar o `ControladorModeracao`, passando a instância do `AgenteClassificador` e do `GerenciadorBancoDados`.
- Configurar as rotas, por meio do método `_configurar_rotas(self)`.
- Exportar a variável app para o `Uvicorn`, usando o método `obter_app(self) -> FastAPI:`

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
      "acao": "Aprovar | Sinalizar | Bloquear",
      "modelo_de_llm": "string | null",
      "provedor_llm": "string | null"
    }
    ```

[@test]: /2-2_Israel/testes/teste_api.py#L1-L40