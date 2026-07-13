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

---

## Implementação da Avaliação (*Script* Científico)

Para garantir o rigor acadêmico da validação das métricas MT01 a MT04, o arquivo `/2-2_Israel/codigo/avaliacao/metricas.py` deve ser construído seguindo as regras abaixo:

### 1. Bibliotecas Obrigatórias
- **Leitura de Dados:** Utilizar exclusivamente a biblioteca `pandas` para carregar e manipular o *dataset*.
- **Cálculo Matemático:** Utilizar exclusivamente o módulo `sklearn.metrics` (da biblioteca `scikit-learn`) para extrair a matriz de confusão e calcular os *scores* (Acurácia, F1-Score e Recall).

### 2. Origem dos Dados (*Ground Truth*)
- O script deve carregar o arquivo CSV do **HateBRXplain**, localizado em `/2-2_Israel/dados/HateBRXplain.csv`.
- A coluna `comment` deve ser utilizada como o texto de entrada para o `AgenteClassificador`.
- A coluna `offensive_label` (onde `1` é ofensivo e `0` é inofensivo) deve ser extraída como o gabarito oficial (*y_true*).

### 3. Lógica de Inferência e Comparação
- O script deve instanciar o `AgenteClassificador` (importado de `codigo.agente.agente_classificador`) e processar os comentários.
- Para evitar *Rate Limits* das APIs (OpenAI/Gemini), o script deve aceitar a execução em lotes menores (ex: um parâmetro para processar apenas as primeiras *N* linhas do CSV).
- A propriedade `eh_ofensivo` do JSON retornado pelo agente (convertida para `1` ou `0`) será utilizada como a previsão do modelo (*y_pred*).

### 4. Relatório de Saída
- O script deve imprimir no terminal um relatório final claro exibindo a Matriz de Confusão e os percentuais alcançados para MT01, MT02, MT03 e MT04, validando se o sistema atingiu os limiares exigidos.

[@test]: /2-2_Israel/testes/teste_classificador.py#L1-L30
[@test]: /2-2_Israel/testes/teste_agente.py#L1-L20
[@test]: /2-2_Israel/testes/teste_api.py#L1-L40