#!/bin/bash

echo "=== Desafio 4: Microsserviços Independentes ==="
echo ""

# Cria a rede
echo "1. Criando rede Docker..."
docker network create microservices-network
echo ""

# Constrói Service A
echo "2. Construindo Service A (Users)..."
cd service-a
docker build -t service-a .
cd ..
echo ""

# Constrói Service B
echo "3. Construindo Service B (User Info)..."
cd service-b
docker build -t service-b .
cd ..
echo ""

# Inicia Service A
echo "4. Iniciando Service A na porta 5001..."
docker run -d \
  --name service-a \
  --network microservices-network \
  -p 5001:5001 \
  service-a
echo ""

# Aguarda Service A iniciar
echo "5. Aguardando Service A iniciar..."
sleep 5
echo ""

# Inicia Service B
echo "6. Iniciando Service B na porta 5002..."
docker run -d \
  --name service-b \
  --network microservices-network \
  -p 5002:5002 \
  -e USER_SERVICE_URL=http://service-a:5001 \
  service-b
echo ""

# Aguarda Service B iniciar
echo "7. Aguardando Service B iniciar..."
sleep 3
echo ""

echo "✓ Microsserviços iniciados com sucesso!"
echo ""
echo "=========================================="
echo "Service A (Users):"
echo "  http://localhost:5001"
echo "  http://localhost:5001/users"
echo ""
echo "Service B (User Info):"
echo "  http://localhost:5002"
echo "  http://localhost:5002/user-info"
echo "  http://localhost:5002/user-summary"
echo ""
echo "Para testar a comunicação:"
echo "  ./test.sh"
echo ""
echo "Para ver logs:"
echo "  docker logs -f service-a"
echo "  docker logs -f service-b"
echo ""
echo "Para limpar:"
echo "  ./cleanup.sh"
echo "=========================================="
