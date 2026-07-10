---
name: arquitetura
description: Arquitetura geral do sistema de moderação.
targets:
  - README.md
---

# Arquitetura do Sistema de Moderação

## Componentes

- **Frontend (*Dashboard*):** Interface *web* para analistas inserirem comentários e visualizarem resultados.
- **API REST:** Expõe o agente de moderação via HTTP.
- **Agente Classificador:** Módulo de IA agnóstico que utiliza os padrões de projeto Estratégia e Fábrica para se comunicar com múltiplos provedores de LLM (Ollama, Gemini, OpenAI) configurados via `.env`.
- **Base de Conhecimento:** *Dataset* HateBRXplain para exemplos de casos de borda e *prompt* estruturado do agente.
- **Logs e Métricas:** Coleta de latência, provedor utilizado, acurácia e ações executadas.

## Fluxo

1. Analista insere comentário no frontend.
2. Frontend chama `POST /moderar` na API.
3. API lê a configuração de ambiente e utiliza a Fábrica para instanciar a Estratégia correspondente ao provedor LLM ativo.
4. API invoca o agente classificador através da interface genérica.
5. Agente retorna classificação binária + nível inferido + justificatva + ação.
6. API salva o resultado no banco, loga a interação e retorna a resposta.
7. Frontend exibe resultado e atualiza o histórico.

[@test]: /2-2_Israel/testes/teste_api.py#L1-L40
[@test]: /2-2_Israel/testes/teste_agente.py#L1-L20