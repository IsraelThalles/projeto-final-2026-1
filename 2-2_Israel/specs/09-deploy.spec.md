---
name: deploy
description: Como implantar o sistema de moderação localmente com suporte a múltiplos provedores de LLM.
targets:
  - /2-2_Israel/Dockerfile
  - /2-2_Israel/docker-compose.yml
  - /2-2_Israel/README.md
---

# Deploy do Sistema de Moderação

## Pré-requisitos

- Docker e Docker Compose instalados.
- Se usar Ollama: Serviço Ollama em execução na máquina hospedeira com o modelo desejado (ex: `qwen3:4b`).
- Se usar Nuvem: Chave de API válida do provedor escolhido (ex: Gemini, OpenAI).

## Configuração

A aplicação deve ser configurada pelo arquivo `.env`. As variáveis necessárias incluem:

- `PROVEDOR_LLM` (valores aceitos: `ollama`, `gemini`, `openai`);
- `OLLAMA_URL` (endereço do host, ex: `http://host.docker.internal:11434`);
- `MODELO_LLM` (modelo a ser executado);
- `CHAVE_DA_API` (opcional se `PROVEDOR_LLM=ollama`);
- `TEMPO_LIMITE_INFERENCIA` (opcional - tempo máximo, em segundos, permitido para uma inferência antes do acionamento do fallback).
- Caminho do banco SQLite e portas de exposição (*Frontend* e API).

## Passos de Deploy

1. Clonar o repositório.
2. Copiar `.env.example` para `.env` e preencher com o provedor e chaves desejadas.
3. Executar `docker-compose up --build -d`.
4. Confirmar pelo *endpoint* de *health* check que a API inicializou corretamente.
5. Acessar o *frontend* via navegador.

## Inicialização e Monitoramento

- O banco SQLite deve ser gerado automaticamente na primeira execução caso não exista.
- A aplicação deve subir independentemente da disponibilidade imediata do LLM, falhando de forma graciosa (*fallback*) apenas no momento da inferência caso o provedor selecionado esteja inacessível.
- Logs estruturados no console contendo latência, provedor utilizado (`modelo_de_llm`), requisição e *timeout*.
