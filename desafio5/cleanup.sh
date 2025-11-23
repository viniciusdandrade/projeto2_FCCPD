#!/bin/bash

echo "=== Limpando ambiente do Desafio 5 ==="
echo ""

# Para e remove os containers
echo "1. Parando e removendo containers..."
docker-compose down

echo ""
echo "2. Removendo volumes (se houver)..."
docker-compose down -v

echo ""
echo "3. Removendo imagens..."
docker rmi desafio5-gateway desafio5-user-service desafio5-order-service 2>/dev/null

echo ""
echo "4. Removendo rede..."
docker network rm desafio5-network 2>/dev/null

echo ""
echo "✓ Limpeza concluída!"
