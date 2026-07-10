---
name: requisitos
description: Requisitos funcionais e não funcionais do sistema de moderação.
targets:
  - README.md
  - /2-2_Israel/dados/data_card.md
---

# Requisitos do Sistema de Moderação

## Requisitos Funcionais

- RF01: O sistema deve receber um comentário em português e classificá-lo estritamente como "Ofensivo" ou "Não Ofensivo" (base HateBRXplain).
- RF02: O sistema deve fornecer uma justificativa resumida (*rationale*) baseada nas evidências extraídas do próprio comentário para explicar sua decisão.
- RF03: O sistema deve sugerir uma ação de moderação baseada na classificação (ex: Aprovar, Sinalizar, Bloquear).
- RF04: O sistema deve expor essas capacidades via API REST.
- RF05: O sistema deve oferecer uma interface web simples para analistas de moderação testarem e visualizarem as inferências.

## Requisitos Não Funcionais

- RNF01: Latência mediana (p50) < 1.5s por chamada ao agente (variável conforme o provedor de LLM configurado localmente ou em nuvem).
- RNF02: F1-score ≥ 0.85 para a classe de comentários ofensivos.
- RNF03: *Rate limiting* de 30 requisições por minuto na API para evitar sobrecarga.
- RNF04: Logs estruturados contendo o texto de entrada, a classificação, a latência e a ação sugerida.
- RNF05: Tratamento de tempo limite excedido configurado para estourar rigorosamente em 5 segundos, independente do provedor de LLM utilizado (degradação graciosa).

[@test]: /2-2_Israel/testes/teste_agente.py#L1-L20
[@test]: /2-2_Israel/testes/teste_classificador.py#L1-L30
[@test]: /2-2_Israel/testes/teste_api.py#L1-L40