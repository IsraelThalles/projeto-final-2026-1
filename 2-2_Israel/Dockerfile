# Utiliza uma imagem oficial do Python otimizada para produção
FROM python:3.11-slim

# Define o diretório de trabalho dentro do contêiner
WORKDIR /app

# Instala dependências nativas do sistema necessárias para compilar bibliotecas
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copia os arquivos de dependência e instala (aproveitando o cache de camadas do Docker)
COPY dependências.txt .
RUN pip install --no-cache-dir -r dependências.txt

# Copia todo o código-fonte para dentro do contêiner
COPY . .

# Expõe as portas de comunicação
EXPOSE 8000 8501