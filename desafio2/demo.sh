#!/bin/bash

echo "=== Demonstração Manual de Persistência ==="
echo ""
echo "Este script demonstra passo a passo a persistência de dados."
echo ""

# Cria volume
echo "PASSO 1: Criando volume..."
docker volume create db-volume
echo "✓ Volume criado"
echo ""

# Build
echo "PASSO 2: Construindo imagem..."
docker build -t desafio2-app -f Dockerfile . -q
echo "✓ Imagem construída"
echo ""

# Primeira execução
echo "PASSO 3: Primeira execução - Criando container 'db-container-1'..."
docker run --name db-container-1 -v db-volume:/data desafio2-app
echo ""
echo "✓ Container executado e finalizado"
echo ""

# Remove o container
echo "PASSO 4: Removendo o container 'db-container-1'..."
docker rm db-container-1
echo "✓ Container removido (mas o volume ainda existe!)"
echo ""

# Segunda execução
echo "PASSO 5: Segunda execução - Criando NOVO container 'db-container-2'..."
echo "Os dados devem persistir mesmo com um novo container!"
echo ""
docker run --name db-container-2 -v db-volume:/data desafio2-app
echo ""
echo "✓ Container executado e finalizado"
echo ""

# Remove o segundo container
echo "PASSO 6: Removendo o container 'db-container-2'..."
docker rm db-container-2
echo "✓ Container removido"
echo ""

# Usa o leitor
echo "PASSO 7: Usando container leitor para verificar dados..."
docker build -t desafio2-reader -f Dockerfile.reader . -q
docker run --rm -v db-volume:/data desafio2-reader
echo ""

echo "=========================================="
echo "CONCLUSÃO:"
echo "Os dados persistiram através de múltiplos containers!"
echo "O volume 'db-volume' mantém os dados independentemente dos containers."
echo ""
echo "Para limpar: ./cleanup.sh"
