#!/bin/bash

echo "=== Desafio 1: Containers em Rede ==="
echo ""

# Criando a rede Docker customizada
echo "1. Criando rede Docker customizada 'desafio1-network'..."
docker network create desafio1-network
echo ""

# Construindo a imagem do servidor
echo "2. Construindo imagem do servidor web..."
docker build -t desafio1-server -f Dockerfile.server .
echo ""

# Construindo a imagem do cliente
echo "3. Construindo imagem do cliente..."
docker build -t desafio1-client -f Dockerfile.client .
echo ""

# Iniciando o container do servidor
echo "4. Iniciando container do servidor (web-server)..."
docker run -d \
  --name web-server \
  --network desafio1-network \
  -p 8080:8080 \
  desafio1-server
echo ""

# Aguarda o servidor iniciar
echo "5. Aguardando servidor iniciar..."
sleep 3
echo ""

# Iniciando o container do cliente
echo "6. Iniciando container do cliente (web-client)..."
docker run -d \
  --name web-client \
  --network desafio1-network \
  desafio1-client
echo ""

echo "✓ Containers iniciados com sucesso!"
echo ""
echo "Para ver os logs:"
echo "  - Servidor: docker logs -f web-server"
echo "  - Cliente:  docker logs -f web-client"
echo ""
echo "Para testar manualmente:"
echo "  curl http://localhost:8080"
echo ""
echo "Para parar e remover:"
echo "  ./cleanup.sh"
