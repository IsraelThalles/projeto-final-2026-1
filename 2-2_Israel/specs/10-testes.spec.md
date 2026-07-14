---
name: testes
description: Estratégia de testes automatizados (unitários, de integração e E2E) para garantir a estabilidade do sistema.
targets:
  - /2-2_Israel/testes/teste_fabrica.py
  - /2-2_Israel/testes/teste_provedores.py
  - /2-2_Israel/testes/teste_agente.py
  - /2-2_Israel/testes/teste_api.py
  - /2-2_Israel/testes/teste_banco.py
---

# Estratégia de Testes

## Tecnologias e Ferramentas

- **Framework de Testes:** `pytest`.
- **Cobertura de Código:** `pytest-cov`.
- **Meta mínima de cobertura:** ≥ 80% para os módulos `codigo.agente`, `codigo.api` e `codigo.llm`.
- **Simulação (Mocking):** `unittest.mock` para isolar dependências externas.
- **Cliente Web:** `TestClient` da biblioteca `fastapi` (suportado pelo `httpx`) para testes de integração das rotas.

## Diretrizes e Contratos de Implementação

### 1. Isolamento de Dependências (Mocking)

- **Proibido custo financeiro:** os testes automatizados não podem, sob nenhuma hipótese, realizar requisições reais para OpenAI, Gemini ou Ollama.
- O método `classificar_texto` da interface `ProvedorLLM` deve ser sempre substituído (*mockado*), retornando objetos `RespostaModeracao` previamente definidos, sem comunicação com provedores externos.
- Os testes devem validar apenas o comportamento da aplicação, independentemente da implementação interna de cada provedor.

### 2. Isolamento de Dados (Banco de Dados)

- O `GerenciadorBancoDados` deve ser *mockado* ou configurado para utilizar um banco SQLite em memória (`:memory:`), garantindo isolamento entre os testes e evitando alterações no banco de dados da aplicação.

### 3. Escopo dos Testes

#### Unitários: `teste_fabrica.py`

- Validar se a `FabricaProvedorLLM` retorna a implementação correta quando `PROVEDOR_LLM` for configurado como `openai`, `gemini` ou `ollama`.
- Validar se uma exceção (`ValueError`) é lançada quando um provedor desconhecido for informado.
- Validar se uma exceção apropriada é lançada quando a configuração obrigatória do provedor estiver ausente ou inválida.

#### Unitários: `teste_provedores.py`

- Mockar os clientes OpenAI, Gemini e Ollama para validar a conversão de respostas JSON em `RespostaModeracao`, sem realizar requisições de rede.
- Validar os erros de configuração obrigatória e de resposta vazia ou inválida de cada provedor.

#### Integração: `teste_banco.py`

- Configurar o `GerenciadorBancoDados` com um arquivo SQLite temporário por teste.
- Validar inserção, listagem e filtros por `eh_ofensivo` e `acao`, sem usar o banco da aplicação.

#### Integração: `teste_agente.py`

- Mockar a resposta do LLM simulando diferentes cenários:
  - comentário ofensivo;
  - comentário não ofensivo;
  - discurso de ódio;
  - resposta inválida do modelo.
- Validar a conversão correta para o objeto `RespostaModeracao`.
- Simular erro de comunicação ou *timeout* do provedor e verificar se o *fallback* retorna uma resposta segura contendo justificativa técnica e ação `Sinalizar`.
- Validar que o tempo limite configurado para inferência aciona corretamente o mecanismo de *fallback*.

#### End-to-End (E2E): `teste_api.py`

- Instanciar um `TestClient(app)`.
- Enviar uma requisição `POST /moderar` contendo um comentário válido e verificar:
  - código HTTP `200 OK`;
  - conformidade do JSON com o contrato definido em `esquemas.spec.md`.
- Enviar uma requisição inválida (texto vazio, apenas espaços ou *payload* malformado) e verificar se a API retorna o erro de validação apropriado.
- Enviar uma requisição `GET /historico` e validar:
  - código HTTP esperado;
  - retorno de uma lista de objetos compatível com o contrato da API.

## Execução

O comando oficial para executar e validar toda a suíte de testes na raiz do projeto deve ser:

```bash
pytest testes -v --cov=codigo --cov-report=term-missing
```
