---
name: metricas
description: Métricas utilizadas para avaliar a qualidade do sistema de moderação.
targets:
  - README.md
  - /2-2_Israel/codigo/avaliacao/metricas.py
---

# Métricas de Sucesso

## Qualidade do Modelo (Referência: HateBRXplain)

- MT01: *F1-score* ≥ 0.85 para a classe positiva (comentários ofensivos).
- MT02: *Recall* ≥ 0.90 para a classe positiva, minimizando o risco de falsos negativos passarem pela moderação.
- MT03: Taxa de falsos positivos ≤ 10% (para evitar silenciamento indevido de usuários).
- MT04: Acurácia geral do sistema ≥ 85%.

## Desempenho do Sistema

- MT05: Latência mediana (p50) inferior a 1,5 s por requisição ao agente.
- MT06: Latência de cauda (p95) inferior a 3 s.
- MT07: *Timeout* de segurança da API acionado rigorosamente aos 5 s para qualquer provedor.

## Qualidade da API e Rastreabilidade

- MT08: 100% das respostas devem seguir o contrato JSON definido pela API, independentemente da entrada ou do provedor LLM.
- MT09: Todas as requisições devem gerar logs estruturados e auditáveis contendo *timestamp*, classificação, ação sugerida e tempo total de processamento.

---

# Implementação da Avaliação (*Script* Científico)

Para garantir o rigor da avaliação das métricas MT01 a MT04, o arquivo `/2-2_Israel/codigo/avaliacao/metricas.py` deve ser implementado conforme as regras abaixo.

## 1. Bibliotecas Obrigatórias

- Utilizar `pandas` para leitura e manipulação do *dataset*.
- Utilizar `pathlib.Path` para localizar arquivos do projeto.
- Utilizar `argparse` para configuração da execução via linha de comando.
- Utilizar `time` para controlar o atraso entre requisições.
- Utilizar exclusivamente as funções `accuracy_score`, `f1_score`, `recall_score` e `confusion_matrix` do módulo `sklearn.metrics` para o cálculo das métricas.

## 2. Origem dos Dados (*Ground Truth*)

- O *dataset* deve ser carregado do arquivo `/2-2_Israel/dados/HateBRXplain.csv`.
- A coluna `comment` deve ser utilizada como entrada para o `AgenteClassificador`.
- A coluna `offensive_label` deve ser utilizada como gabarito oficial (*y_true*).

## 3. Estratégia de Amostragem

- O script deve aceitar um parâmetro de linha de comando (`--amostras`) para limitar a quantidade de comentários avaliados.
- Caso o valor informado seja maior que o tamanho do *dataset*, deve ser utilizado todo o conjunto disponível.
- A seleção das amostras deve ser feita por **amostragem aleatória estratificada**, preservando a proporção entre comentários ofensivos e não ofensivos.
- A amostragem deve utilizar `random_state=42` para garantir reprodutibilidade dos resultados.

## 4. Processo de Inferência

- O script deve instanciar exatamente uma instância de `AgenteClassificador`.
- Cada comentário selecionado deve ser enviado ao método `moderar_comentario`.
- O campo `eh_ofensivo` retornado pelo agente deve ser convertido para `1` (ofensivo) ou `0` (não ofensivo), formando o vetor de previsões (*y_pred*).
- O script deve aceitar um parâmetro (`--atraso`) para definir o intervalo, em segundos, entre as requisições ao modelo, permitindo evitar *rate limits* em provedores externos.
- Caso ocorra qualquer exceção durante a inferência, o script deve:
  - registrar a falha no terminal;
  - aplicar *fallback* classificando a amostra como não ofensiva (`0`);
  - continuar normalmente a avaliação das demais amostras.

## 5. Cálculo das Métricas

Após concluir todas as inferências, o script deve calcular:

- Acurácia Geral (MT04);
- F1-Score (MT01);
- Recall (MT02);
- Matriz de Confusão;
- Taxa de Falsos Positivos (MT03), calculada como:

```
FP / (FP + TN)
```

## 6. Relatório de Saída

Ao final da execução, o script deve imprimir um relatório contendo:

- Quantidade de amostras avaliadas;
- Matriz de Confusão completa;
- Quantidade de:
  - Verdadeiros Positivos;
  - Verdadeiros Negativos;
  - Falsos Positivos;
  - Falsos Negativos;
- Valor obtido para MT01, MT02, MT03 e MT04;
- Indicação visual (✅ ou ❌) informando se cada métrica atingiu o limite estabelecido na especificação.

[@test]: /2-2_Israel/testes/teste_classificador.py#L1-L30
[@test]: /2-2_Israel/testes/teste_agente.py#L1-L20
[@test]: /2-2_Israel/testes/teste_api.py#L1-L40