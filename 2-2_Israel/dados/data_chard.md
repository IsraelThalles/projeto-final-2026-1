# Data Card

## Nome

HateBRXplain

## Descrição

Conjunto de dados em português destinado à detecção de discurso de ódio e linguagem ofensiva em redes sociais.

## Origem

HateBRXplain Dataset

Artigo:

> HateBRXplain: A Benchmark Dataset for Explainable Hate Speech Detection in Brazilian Portuguese.

## Fonte

https://huggingface.co/datasets/HateBR/HateBRXplain

## Licença

Conforme disponibilizada pelos autores do conjunto de dados.

## Utilização neste projeto

O conjunto de dados foi utilizado exclusivamente para avaliação do desempenho do agente de moderação.

Foram utilizadas as colunas:

- `comment`
- `offensive_label`

A coluna `comment` fornece o texto analisado pelo agente.

A coluna `offensive_label` é utilizada como verdade de referência (*ground truth*) para comparação com as predições do sistema.

## Pré-processamento

Nenhum pré-processamento significativo foi realizado.

Os comentários foram utilizados conforme disponibilizados pelos autores.

## Limitações

- O conjunto representa apenas uma amostra da linguagem utilizada em plataformas online brasileiras.
- Pode conter vieses inerentes ao processo de anotação humana.
- Não representa todos os dialetos, contextos sociais ou tipos de discurso existentes.

## Finalidade

Avaliação das métricas:

- Acurácia
- Recall
- F1-Score
- Taxa de Falsos Positivos