#!/bin/bash

echo "=== Testando API Gateway e Microsserviços ==="
echo ""

GATEWAY_URL="http://localhost:5000"

# Teste 1: Informações do Gateway
echo "1. Informações do API Gateway:"
curl -s $GATEWAY_URL/ | jq '{service, version, description}'
echo ""

# Teste 2: Health Check
echo "2. Health Check de todos os serviços:"
curl -s $GATEWAY_URL/health | jq '.'
echo ""

# Teste 3: Listar usuários via Gateway
echo "3. Listar usuários (via Gateway → User Service):"
curl -s $GATEWAY_URL/users | jq '{via, service, count, sample: .users[0]}'
echo ""

# Teste 4: Detalhes de usuário via Gateway
echo "4. Detalhes de usuário específico:"
curl -s $GATEWAY_URL/users/1 | jq '{via, user: .user}'
echo ""

# Teste 5: Listar pedidos via Gateway
echo "5. Listar pedidos (via Gateway → Order Service):"
curl -s $GATEWAY_URL/orders | jq '{via, service, count, sample: .orders[0]}'
echo ""

# Teste 6: Detalhes de pedido via Gateway
echo "6. Detalhes de pedido específico:"
curl -s $GATEWAY_URL/orders/1 | jq '{via, order: .order}'
echo ""

# Teste 7: AGREGAÇÃO - O grande diferencial!
echo "7. AGREGAÇÃO: Dados completos de usuário (usuário + pedidos):"
echo "   Este endpoint combina dados de DOIS microsserviços!"
curl -s $GATEWAY_URL/users/1/complete | jq '{
  via,
  aggregated_from,
  user_name: .user.user.name,
  user_email: .user.user.email,
  total_orders: .orders_summary.total_orders,
  total_spent: .orders_summary.total_spent
}'
echo ""

# Teste 8: Estatísticas do Gateway
echo "8. Estatísticas de uso do Gateway:"
curl -s $GATEWAY_URL/stats | jq '.statistics'
echo ""

echo "=========================================="
echo "✓ Testes concluídos!"
echo ""
echo "DEMONSTRAÇÃO:"
echo "1. Todos os acessos passaram pelo API Gateway (porta 5000)"
echo "2. O Gateway roteou requisições para os microsserviços corretos"
echo "3. O endpoint /users/1/complete demonstra AGREGAÇÃO:"
echo "   - Gateway consultou user-service"
echo "   - Gateway consultou order-service"
echo "   - Gateway combinou os dados em uma única resposta"
echo "4. Cliente não precisa conhecer os microsserviços individuais"
echo "=========================================="
