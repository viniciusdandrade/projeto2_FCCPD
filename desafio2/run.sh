#!/bin/bash

echo "=== Desafio 2: Volumes e Persistência ==="
echo ""

# Cria um volume nomeado
echo "1. Criando volume Docker 'db-volume'..."
docker volume create db-volume
echo ""

# Construindo a imagem principal
echo "2. Construindo imagem da aplicação..."
docker build -t desafio2-app -f Dockerfile .
echo ""

# Construindo a imagem do leitor
echo "3. Construindo imagem do leitor..."
docker build -t desafio2-reader -f Dockerfile.reader .
echo ""

# Primeira execução - Cria dados
echo "4. Executando aplicação pela PRIMEIRA vez (criando dados)..."
docker run --rm \
  --name db-writer \
  -v db-volume:/data \
  desafio2-app
echo ""

echo "=== DEMONSTRAÇÃO DE PERSISTÊNCIA ==="
echo ""
echo "Os dados foram gravados no volume 'db-volume'."
echo "Agora vamos provar a persistência removendo e recriando o container..."
echo ""

read -p "Pressione ENTER para continuar..."
echo ""

# Segunda execução - Dados persistem
echo "5. Executando aplicação pela SEGUNDA vez (dados devem persistir)..."
docker run --rm \
  --name db-writer \
  -v db-volume:/data \
  desafio2-app
echo ""

echo "=== LEITURA COM CONTAINER SEPARADO ==="
echo ""
echo "Agora vamos ler os dados usando um container DIFERENTE..."
echo ""

# Executa o leitor
echo "6. Executando container leitor..."
docker run --rm \
  --name db-reader \
  -v db-volume:/data \
  desafio2-reader
echo ""

echo "✓ Demonstração completa!"
echo ""
echo "Comandos úteis:"
echo "  - Inspecionar volume: docker volume inspect db-volume"
echo "  - Ver localização no host: docker volume inspect db-volume | grep Mountpoint"
echo "  - Listar volumes: docker volume ls"
echo "  - Remover tudo: ./cleanup.sh"
