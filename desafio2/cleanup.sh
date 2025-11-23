#!/bin/bash

echo "=== Limpando ambiente do Desafio 2 ==="
echo ""

# Para e remove containers se existirem
echo "1. Removendo containers..."
docker rm -f db-writer db-reader db-container-1 db-container-2 2>/dev/null
echo ""

# Remove as imagens
echo "2. Removendo imagens..."
docker rmi desafio2-app desafio2-reader 2>/dev/null
echo ""

# Remove o volume
echo "3. Removendo volume..."
docker volume rm db-volume 2>/dev/null
echo ""

echo "✓ Limpeza concluída!"
