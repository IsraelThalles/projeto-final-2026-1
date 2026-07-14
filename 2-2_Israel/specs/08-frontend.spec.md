---
name: frontend
description: Interface web (dashboard) interativa construída com Streamlit que consome a API de moderação.
targets:
  - /2-2_Israel/codigo/aplicativo/app.py
---

# Produto: Painel de Moderação de Comentários

## Tecnologia e Arquitetura

- **Framework Visual:** Streamlit (`streamlit`).
- **Comunicação com API:** Biblioteca `requests` para realizar chamadas HTTP ao backend FastAPI.
- O frontend não deve acessar diretamente o banco de dados nem importar classes do módulo `codigo.banco`. Toda comunicação deve ocorrer exclusivamente por meio da API REST.

## Contratos de Implementação

A aplicação deve ser contida em um único script e executada via:

```bash
streamlit run codigo/aplicativo/app.py
```

A URL da API deve ser obtida da variável de ambiente `API_URL`, utilizando `http://localhost:8000` como valor padrão.

### 1. Configuração da Página e UX

- A página deve utilizar `st.set_page_config` com um título adequado e layout amigável.
- Deve possuir um cabeçalho claro explicando o propósito da ferramenta (ex.: "Shield IA - Moderação de Conteúdo").

### 2. Área de Inferência (Tempo Real)

- **Entrada:** Um campo `st.text_area` para o analista colar ou digitar um comentário suspeito.
- **Ação:** Um botão `st.button("Analisar Toxicidade")`.
- **Estado de Carregamento:** Ao clicar no botão, a interface deve exibir um `st.spinner("A IA está analisando o texto...")` até o término da requisição.
- **Integração:** O script deve realizar uma requisição `POST` para `/moderar`, enviando o payload JSON:

```json
{
    "texto": "comentário digitado"
}
```

- Após uma classificação realizada com sucesso, a interface deve atualizar automaticamente a tabela de histórico.
- **Tratamento de Erros:** Exibir `st.error()` com uma mensagem amigável caso a requisição exceda o tempo limite configurado para inferência ou a API esteja indisponível.

### 3. Painel de Resultados (Card de Resposta)

O JSON retornado pela API deve ser renderizado utilizando componentes do Streamlit.

#### Indicador de Ação

- Se `acao == "Aprovar"` utilizar `st.success()`.
- Se `acao == "Sinalizar"` utilizar `st.warning()`.
- Se `acao == "Bloquear"` utilizar `st.error()`.

#### Informações da Classificação

Utilizar duas colunas (`st.columns(2)`):

- **Coluna 1:** Nível da Ofensa.
- **Coluna 2:** Discurso de Ódio (Sim ou Não).

#### Justificativa

Exibir a justificativa retornada pelo agente utilizando `st.info()`.

### 4. Histórico de Análises

- O dashboard deve possuir um subcabeçalho (ex.: "Últimas Análises").
- O histórico deve ser obtido exclusivamente através da API utilizando uma requisição `GET /historico`.
- A resposta deve ser convertida para um `DataFrame` do Pandas.
- O histórico deve ser exibido utilizando `st.dataframe()`, permitindo ordenação e filtros nativos.
- A tabela deve exibir, no mínimo, as seguintes colunas:
  - Data/Hora;
  - Comentário;
  - Ofensivo;
  - Nível da Ofensa;
  - Discurso de Ódio;
  - Ação.
