# Usa a imagem base python slim
FROM python:3.9-slim

# Define o diretório de trabalho no contêiner
WORKDIR /app

# Copia os arquivos necessários para o diretório de trabalho
COPY . .

# Instala as dependências diretamente
RUN pip install requests websocket-client pydantic

# Define o comando padrão para rodar o script client.py
CMD ["python", "client.py"]
