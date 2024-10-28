# Usa uma imagem base do Python
FROM python:3.9-slim

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia os arquivos de dependências para o container
COPY requirements.txt .

# Instala as dependências do Python
RUN pip install --no-cache-dir -r requirements.txt

# Copia a pasta src com o código do bot para o diretório de trabalho no container
COPY src/ ./src/

# Define o comando para rodar o bot (ajuste conforme seu código)
CMD ["python", "./src/main.py"]