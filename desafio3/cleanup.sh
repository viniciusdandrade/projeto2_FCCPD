#!/bin/bash

echo "=== Limpando ambiente do Desafio 3 ==="
echo ""

# Para e remove os containers
echo "1. Parando e removendo containers..."
docker-compose down

echo ""
echo "2. Removendo volumes..."
docker-compose down -v

echo ""
echo "3. Removendo imagens..."
docker rmi desafio3-web 2>/dev/null

echo ""
echo "4. Removendo rede..."
docker network rm desafio3-network 2>/dev/null

echo ""
echo "✓ Limpeza concluída!"
