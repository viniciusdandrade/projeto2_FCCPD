FROM python:3.11-slim

WORKDIR /app

RUN pip install --no-cache-dir flask requests

COPY app.py .

EXPOSE 5000

ENV PORT=5000
ENV USER_SERVICE_URL=http://user-service:5001
ENV ORDER_SERVICE_URL=http://order-service:5002

CMD ["python", "app.py"]
