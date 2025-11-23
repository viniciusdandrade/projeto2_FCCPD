#!/bin/bash

echo "=== Limpando ambiente do Desafio 4 ==="
echo ""

# Para e remove os containers
echo "1. Parando e removendo containers..."
docker stop service-a service-b 2>/dev/null
docker rm service-a service-b 2>/dev/null
echo ""

# Remove as imagens
echo "2. Removendo imagens..."
docker rmi service-a service-b 2>/dev/null
echo ""

# Remove a rede
echo "3. Removendo rede..."
docker network rm microservices-network 2>/dev/null
echo ""

echo "✓ Limpeza concluída!"
