---
name: agente_classificador
description: Agente de IA agnóstico que detecta toxicidade em comentários em português e explica o raciocínio.
targets:
  - /2-2_Israel/codigo/agente/agente_classificador.py
  - /2-2_Israel/codigo/llm/cliente.py
  - /2-2_Israel/codigo/llm/fabrica.py
  - /2-2_Israel/codigo/llm/provedores/openai.py
  - /2-2_Israel/codigo/llm/provedores/gemini.py
  - /2-2_Israel/codigo/llm/provedores/ollama.py
  - /2-2_Israel/codigo/llm/prompts/prompt_sistema.md
---

# Agente Classificador de Toxicidade (Moderação)

## Capacidades

- Receber um comentário de rede social em português e classificar sua toxicidade.
- **Classificação Binária Principal:** Determinar se é Ofensivo ou Não Ofensivo.
- **Inferência de Nível:** Determinar o nível de ofensa (altamente, moderadamente, levemente) baseado na quantidade e peso dos termos pejorativos, seguindo a árvore de decisão estruturada do HateBR.
- **Inferência de Ódio:** Identificar se a ofensa se enquadra como discurso de ódio (booleano).
- Justificar a classificação em linguagem natural baseada no texto.
- Sugerir ação de moderação (Aprovar, Sinalizar ou Bloquear).

## Estrutura e Responsabilidades dos Arquivos

Para garantir a modularidade e respeitar os Padrões de Projeto (Estratégia e Fábrica), o código deve ser gerado separadamente nos arquivos correspondentes:

### 1. O Prompt do Sistema (`/2-2_Israel/codigo/llm/prompts/prompt_sistema.md`)

Arquivo de texto estático que o agente Python deverá ler em tempo de execução. Ele deve conter a Árvore de decisão do HateBRXplain descrita abaixo.

### 2. Interface (`/2-2_Israel/codigo/llm/cliente.py`)

Deve conter apenas a classe abstrata/interface `ProvedorLLM` que define o contrato base (método de classificação) para todos os modelos.

### 3. Implementações Concretas (`/2-2_Israel/codigo/llm/provedores/`)

- `openai.py`: Implementa a classe `EstratégiaOpenAI`.
- `gemini.py`: Implementa a classe `EstratégiaGemini`.
- `ollama.py`: Implementa a classe `EstratégiaOllama`.

*Regra:* Todas as implementações devem retornar exatamente a estrutura definida pelo esquema de resposta do sistema em `codigo/esquemas/esquemas.py`.

### 4. Fábrica (`/2-2_Israel/codigo/llm/fabrica.py`)

Deve conter a `FábricaProvedorLLM`, responsável por ler o arquivo `.env` e instanciar dinamicamente a estratégia correta.
A fábrica não deve conter lógica de comunicação com APIs nem construção de prompts.
Sua única responsabilidade é selecionar e instanciar o provedor apropriado.

### 5. Agente Principal (`/2-2_Israel/codigo/agente/agente_classificador.py`)

O orquestrador do sistema. Ele deve:
1. Ler o conteúdo de `prompt_sistema.md`.
2. Instanciar o modelo via Fábrica.
3. Executar a chamada de classificação com o *Guardrail* de *Fallback* (se exceder 5 segundos ou falhar, deve retornar ação "Sinalizar" com justificativa de erro técnico).

O agente principal não deve conhecer detalhes dos provedores.

Toda comunicação com o modelo deve ocorrer exclusivamente através da interface ProvedorLLM.

---

## Conteúdo exigido para o arquivo `prompt_sistema.md`

O arquivo de texto do *prompt* deve ser gerado contendo exatamente estas instruções para o LLM:

**Árvore de decisão**

O agente deve realizar a classificação seguindo obrigatoriamente a sequência abaixo.

*Etapa 1 — Linguagem Ofensiva*

Determinar se o comentário contém pelo menos um termo ou expressão com conotação pejorativa.
- Caso não contenha, classificar como não ofensivo e encerrar a análise.
- Caso contenha, prosseguir para a classificação do nível de ofensividade.

*Etapa 2 — Nível de Ofensividade*

Caso o comentário seja ofensivo, determinar sua gravidade.

Classificar como altamente ofensivo quando ocorrer qualquer uma das situações:
- sequência de palavrões;
- sequência de três ou mais termos ou expressões pejorativas, explícitas ou implícitas.

Caso contrário:
- se houver duas ou mais expressões pejorativas, classificar como moderadamente ofensivo;
- caso contrário, classificar como levemente ofensivo.

*Etapa 3 — Discurso de Ódio*

Após determinar o nível de ofensividade, verificar se os termos ofensivos são direcionados a um grupo protegido.
Exemplos: raça, etnia, religião, nacionalidade, gênero, orientação sexual, deficiência.
Caso positivo, classificar como discurso de ódio.

*Etapa 4 — Resposta Final*

O agente deve retornar um JSON contendo, no mínimo:
- classificação ofensiva;
- nível da ofensa;
- indicação de discurso de ódio;
- justificativa;
- ação recomendada.

---

[@test]: /2-2_Israel/testes/teste_agente.py#L21-L50
[@test]: /2-2_Israel/testes/teste_classificador.py#L31-L60