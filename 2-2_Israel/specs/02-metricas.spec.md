---
name: metricas
description: Métricas utilizadas para avaliar a qualidade do sistema de moderação.
targets:
  - README.md
  - /2-2_Israel/codigo/avaliacao/metricas.py
---

# Métricas de Sucesso

## Qualidade do Modelo (Referência: HateBRXplain)

- MT01: *F1-score* ≥ 0.85 para a classe positiva (comentários Ofensivos).
- MT02: *Recall* ≥ 0.90 para a classe positiva, minimizando o risco de falsos negativos passarem pela moderação.
- MT03: Taxa de falsos positivos ≤ 10% (para evitar silenciamento indevido de usuários).
- MT04: Acurácia geral do sistema ≥ 85%.

## Desempenho do Sistema

- MT05: Latência mediana (p50) inferior a 1.5s por requisição ao agente.
- MT06: Latência de cauda (p95) inferior a 3 segundos.
- MT07: *Timeout* de segurança da API acionado rigorosamente aos 5 segundos para qualquer provedor.

## Qualidade da API e Rastreabilidade

- MT08: 100% das respostas devem seguir o contrato JSON definido pela API, independentemente da entrada ou provedor LLM.
- MT09: Todas as requisições devem gerar logs estruturados e auditáveis contendo: *timestamp*, comentário, classificação, ação sugerida e tempo total de processamento.

[@test]: /2-2_Israel/testes/teste_classificador.py#L1-L30
[@test]: /2-2_Israel/testes/teste_agente.py#L1-L20
[@test]: /2-2_Israel/testes/teste_api.py#L1-L40