---
name: esquemas
description: Definição dos contratos de dados (Pydantic models) e enums utilizados em todo o sistema.
targets:
  - /2-2_Israel/codigo/esquemas/esquemas.py
---

# Especificação de Esquemas de Dados

## Enums

* **NivelDaOfensa**:
    * `nenhuma`: "nenhuma"
    * `levemente`: "levemente"
    * `moderadamente`: "moderadamente"
    * `altamente`: "altamente"
* **Acao**:
    * `Aprovar`: "Aprovar"
    * `Sinalizar`: "Sinalizar"
    * `Bloquear`: "Bloquear"

## Modelos Pydantic

### ComentarioEntrada
* `texto` (str): O texto do comentário a ser moderado.

### RespostaModeracao
* `eh_ofensivo` (bool): Indica se o comentário é ofensivo.
* `nivel_da_ofensa` (NivelDaOfensa): O nível da ofensa do comentário.
* `eh_discurso_de_odio` (bool): Indica se o comentário contém discurso de ódio.
* `justificativa` (str): A justificativa para a classificação.
* `acao` (Acao): A ação recomendada para o comentário.
* `modelo_de_llm` (Optional[str]): O modelo de LLM utilizado para a moderação (padrão: None).
* `provedor_llm` (Optional[str]): O provedor do LLM utilizado para a moderação (padrão: None).

### ComentarioSaidaBanco (Herda de RespostaModeracao)
* `id` (int): O ID único do comentário no banco de dados.
* `texto` (str): O texto original do comentário.
* `criado_em` (Optional[datetime]): O timestamp de criação do registro (padrão: None).