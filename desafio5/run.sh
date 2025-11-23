#!/bin/bash

echo "=== Desafio 5: Microsserviços com API Gateway ==="
echo ""

# Inicia todos os serviços com Docker Compose
echo "Iniciando serviços com Docker Compose..."
docker-compose up -d --build

echo ""
echo "Aguardando serviços ficarem prontos..."
sleep 10

echo ""
echo "Status dos containers:"
docker-compose ps

echo ""
echo "✓ Sistema iniciado com sucesso!"
echo ""
echo "=========================================="
echo "API Gateway (ponto único de entrada):"
echo "  http://localhost:5000"
echo ""
echo "Endpoints disponíveis via Gateway:"
echo "  GET  http://localhost:5000/           - Info do gateway"
echo "  GET  http://localhost:5000/health     - Health de todos os serviços"
echo "  GET  http://localhost:5000/stats      - Estatísticas do gateway"
echo "  GET  http://localhost:5000/users      - Lista usuários"
echo "  GET  http://localhost:5000/users/1    - Detalhes de usuário"
echo "  GET  http://localhost:5000/orders     - Lista pedidos"
echo "  GET  http://localhost:5000/orders/1   - Detalhes de pedido"
echo "  GET  http://localhost:5000/users/1/complete - Dados agregados!"
echo ""
echo "Microsserviços (acesso direto - apenas para teste):"
echo "  User Service:  http://localhost:5001 (não exposto via gateway)"
echo "  Order Service: http://localhost:5002 (não exposto via gateway)"
echo ""
echo "Comandos úteis:"
echo "  docker-compose logs -f           - Ver logs"
echo "  docker-compose logs -f gateway   - Logs do gateway"
echo "  ./test.sh                        - Executar testes"
echo "  docker-compose down              - Parar tudo"
echo "=========================================="
