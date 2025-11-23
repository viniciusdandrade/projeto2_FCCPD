#!/bin/bash

echo "Cliente iniciando requisições periódicas..."
echo "Servidor alvo: http://web-server:8080"
echo "========================================="

# Loop infinito fazendo requisições a cada 5 segundos
while true; do
    echo ""
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Fazendo requisição ao servidor..."
    
    # Faz a requisição e captura a resposta
    response=$(curl -s http://web-server:8080)
    
    if [ $? -eq 0 ]; then
        echo "✓ Resposta recebida:"
        echo "$response" | jq '.'
    else
        echo "✗ Erro ao conectar ao servidor"
    fi
    
    echo "Aguardando 5 segundos..."
    sleep 5
done
