FROM python:3.11-slim

WORKDIR /app

# Instala Flask
RUN pip install --no-cache-dir flask requests

# Copia o código do serviço
COPY app.py .

# Expõe a porta 5001
EXPOSE 5001

# Define variável de ambiente
ENV PORT=5001

# Comando para iniciar o serviço
CMD ["python", "app.py"]
