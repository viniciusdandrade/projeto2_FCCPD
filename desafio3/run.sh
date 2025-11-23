#!/bin/bash

echo "=== Desafio 3: Docker Compose - Orquestrando Serviços ==="
echo ""

# Inicia os serviços
echo "Iniciando serviços com Docker Compose..."
docker-compose up -d

echo ""
echo "Aguardando serviços ficarem prontos..."
sleep 10

echo ""
echo "✓ Serviços iniciados!"
echo ""
echo "Status dos containers:"
docker-compose ps

echo ""
echo "=========================================="
echo "Aplicação disponível em:"
echo "  http://localhost:5000"
echo ""
echo "Endpoints disponíveis:"
echo "  GET  http://localhost:5000/         - Informações do sistema"
echo "  GET  http://localhost:5000/health   - Health check"
echo "  GET  http://localhost:5000/users    - Lista usuários"
echo "  POST http://localhost:5000/users    - Cria usuário"
echo "  GET  http://localhost:5000/stats    - Estatísticas"
echo ""
echo "Comandos úteis:"
echo "  docker-compose logs -f        - Ver logs de todos os serviços"
echo "  docker-compose logs -f web    - Ver logs apenas do web"
echo "  docker-compose ps             - Status dos containers"
echo "  docker-compose down           - Parar todos os serviços"
echo "  ./cleanup.sh                  - Limpar tudo"
echo "=========================================="
