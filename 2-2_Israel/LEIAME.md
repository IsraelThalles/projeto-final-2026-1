# 🛡️ Shield IA - Moderação de Conteúdo

Sistema automatizado de moderação de comentários focado na detecção de discursos de ódio e toxicidade, utilizando grandes modelos de linguagem (LLMs).

## 🚀 Arquitetura do Sistema

- **Backend:** API RESTful construída com FastAPI.
- **Frontend:** Dashboard interativo em Streamlit.
- **Banco de Dados:** SQLite nativo para persistência de histórico e auditoria.
- **Motor de IA:** Suporte dinâmico (Strategy) para execução local via Ollama ou em nuvem (OpenAI / Google Gemini).

## ⚙️ Como Executar com Docker

1. Crie o seu arquivo de variáveis de ambiente:
```bash
cp .env.example .env
```

2. Edite o arquivo `.env` com suas chaves e o provedor LLM escolhido.

3. Suba os contêineres desativando o BuildKit para evitar problemas de rede (IPv6):
```bash
docker-compose up --build -d
```
4. Acesse o painel pelo navegador:
```
http://localhost:8501
```


5. Acesse a documentação da API:
```
http://localhost:8000/docs
```

## 💻 Como Executar sem Docker

1. Crie e ative um ambiente virtual na raiz do projeto, depois instale as dependências:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r dependências.txt
```

2. Crie o arquivo de configuração e preencha-o para o provedor LLM desejado:

```bash
cp .env.example .env
```

Para usar Ollama local, mantenha o serviço e o modelo configurado em `.env` disponíveis antes de enviar uma moderação.

3. Em um terminal, inicie a API. A mudança para `codigo` é necessária para que os imports dos módulos da aplicação sejam encontrados:

```bash
cd codigo
uvicorn api.app:app --reload
```

4. Em outro terminal, com o ambiente virtual ativado e na raiz do projeto, inicie o frontend:

```bash
streamlit run codigo/aplicativo/app.py
```

5. Acesse o painel em `http://localhost:8501` ou a documentação da API em `http://localhost:8000/docs`.

## 🧪 Como Executar os Testes

Para garantir que o código cumpra as metas de negócio, execute a suíte de testes:
```bash
pytest testes/ -v --cov=codigo --cov-report=term-missing
```

## 📊 Como Executar as Métricas (Avaliador Científico)

Para rodar a suíte de avaliação e extrair as métricas de performance do modelo de IA (como Precision, Recall e F1-Score) contra o dataset HateBRXplain, execute no terminal:
```bash
python codigo/avaliacao/metricas.py
```
## 🛑 Encerrando a Aplicação

Para desligar os serviços, utilize:
```bash
docker-compose down
```
