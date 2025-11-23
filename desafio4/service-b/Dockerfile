FROM python:3.11-slim

WORKDIR /app

# Instala Flask e requests
RUN pip install --no-cache-dir flask requests

# Copia o código do serviço
COPY app.py .

# Expõe a porta 5002
EXPOSE 5002

# Define variáveis de ambiente
ENV PORT=5002
ENV USER_SERVICE_URL=http://service-a:5001

# Comando para iniciar o serviço
CMD ["python", "app.py"]
