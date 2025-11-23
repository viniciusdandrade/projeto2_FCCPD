# Dockerfile para a aplicação que escreve no banco
FROM python:3.11-slim

WORKDIR /app

# Copia o código da aplicação
COPY app.py .

# Cria o diretório para o volume
RUN mkdir -p /data

# Define o volume
VOLUME ["/data"]

# Executa a aplicação
CMD ["python", "app.py"]
