#!/bin/bash

echo "=== Testando a comunicação entre serviços ==="
echo ""

BASE_URL="http://localhost:5000"

# Teste 1: Health Check
echo "1. Testando health check..."
curl -s $BASE_URL/health | jq '.'
echo ""

# Teste 2: Listar usuários (do banco de dados)
echo "2. Listando usuários (primeira vez - do banco)..."
curl -s $BASE_URL/users | jq '.'
echo ""

# Teste 3: Listar usuários novamente (do cache)
echo "3. Listando usuários (segunda vez - do cache)..."
curl -s $BASE_URL/users | jq '.'
echo ""

# Teste 4: Criar novo usuário
echo "4. Criando novo usuário..."
curl -s -X POST $BASE_URL/users \
  -H "Content-Type: application/json" \
  -d '{"name": "Teste Docker", "email": "teste@docker.com"}' | jq '.'
echo ""

# Teste 5: Listar usuários após criar novo (cache invalidado)
echo "5. Listando usuários após criar novo..."
curl -s $BASE_URL/users | jq '.'
echo ""

# Teste 6: Testar cache manual
echo "6. Testando cache manualmente..."
echo "  Salvando valor no cache..."
curl -s -X POST $BASE_URL/cache/set \
  -H "Content-Type: application/json" \
  -d '{"key": "teste", "value": "Docker Compose funcionando!", "ttl": 60}' | jq '.'
echo ""

echo "  Recuperando valor do cache..."
curl -s $BASE_URL/cache/get/teste | jq '.'
echo ""

# Teste 7: Estatísticas
echo "7. Verificando estatísticas..."
curl -s $BASE_URL/stats | jq '.'
echo ""

echo "✓ Todos os testes concluídos!"
