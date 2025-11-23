#!/bin/bash

echo "=== Limpando ambiente do Desafio 1 ==="
echo ""

# Para e remove os containers
echo "1. Parando e removendo containers..."
docker stop web-server web-client 2>/dev/null
docker rm web-server web-client 2>/dev/null
echo ""

# Remove as imagens
echo "2. Removendo imagens..."
docker rmi desafio1-server desafio1-client 2>/dev/null
echo ""

# Remove a rede
echo "3. Removendo rede Docker..."
docker network rm desafio1-network 2>/dev/null
echo ""

echo "✓ Limpeza concluída!"
