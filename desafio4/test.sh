#!/bin/bash

echo "=== Testando Comunicação entre Microsserviços ==="
echo ""

# Teste Service A
echo "1. Testando Service A (Users)..."
echo "GET http://localhost:5001/users"
curl -s http://localhost:5001/users | jq '.users | length as $count | "Total de usuários: \($count)"'
echo ""

# Teste Service B buscando informações do Service A
echo "2. Testando Service B (User Info) - Consome Service A..."
echo "GET http://localhost:5002/user-info"
curl -s http://localhost:5002/user-info | jq '{service, source, count, sample_user: .users[0].enriched_info.profile_summary}'
echo ""

# Teste usuário específico
echo "3. Testando informações enriquecidas de usuário específico..."
echo "GET http://localhost:5002/user-info/1"
curl -s http://localhost:5002/user-info/1 | jq '.user | {name, role, enriched: .enriched_info.member_since}'
echo ""

# Teste resumo
echo "4. Testando resumo estatístico..."
echo "GET http://localhost:5002/user-summary"
curl -s http://localhost:5002/user-summary | jq '.summary'
echo ""

# Health checks
echo "5. Verificando health dos serviços..."
echo ""
echo "Service A Health:"
curl -s http://localhost:5001/health | jq '.'
echo ""
echo "Service B Health (verifica conexão com A):"
curl -s http://localhost:5002/health | jq '.'
echo ""

echo "✓ Testes concluídos!"
echo ""
echo "DEMONSTRAÇÃO:"
echo "Service B consumiu dados do Service A e os enriqueceu com:"
echo "  - Cálculo de tempo como membro"
echo "  - Formatação de status"
echo "  - Estatísticas agregadas"
echo "  - Resumos personalizados"
