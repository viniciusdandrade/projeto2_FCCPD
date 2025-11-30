# Desafio 5 - Microsserviços com API Gateway

## Descrição

Este desafio implementa uma arquitetura completa de microsserviços com API Gateway. O gateway atua como ponto único de entrada, centralizando o acesso a dois microsserviços independentes (usuários e pedidos), além de fornecer funcionalidades de agregação de dados.

## Arquitetura

```
                          ┌─────────────────────┐
                          │       Cliente       │
                          └──────────┬──────────┘
                                     │
                                     │ HTTP
                                     │
                          ┌──────────▼──────────┐
                          │    API Gateway      │
                          │      :5000          │
                          │                     │
                          │  - Roteamento       │
                          │  - Agregação        │
                          │  - Health Check     │
                          │  - Estatísticas     │
                          └──────────┬──────────┘
                                     │
                    ┌────────────────┴────────────────┐
                    │                                 │
         ┌──────────▼──────────┐         ┌──────────▼──────────┐
         │   User Service      │         │   Order Service     │
         │      :5001          │         │       :5002         │
         │                     │         │                     │
         │  - Gerencia         │         │  - Gerencia         │
         │    usuários         │         │    pedidos          │
         │  - CRUD users       │         │  - CRUD orders      │
         └─────────────────────┘         └─────────────────────┘

         Network: desafio5-network (internal)
```

### Fluxo de Requisição

```
1. Cliente faz requisição → http://localhost:5000/users
2. API Gateway recebe
3. Gateway roteia para → http://user-service:5001/users
4. User Service processa e responde
5. Gateway adiciona metadados e retorna ao cliente
```

### Componentes:

#### **API Gateway** (Porta 5000)

- **Função**: Ponto único de entrada (Single Entry Point)
- **Responsabilidades**:
  - Roteamento de requisições
  - Agregação de dados de múltiplos serviços
  - Health checking de todos os serviços
  - Estatísticas de uso
  - Potencial para: autenticação, rate limiting, logging

**Endpoints:**

- `GET /` - Informações do gateway
- `GET /health` - Health check de todos os serviços
- `GET /stats` - Estatísticas de uso
- `GET /users` - Proxy para user-service
- `GET /users/<id>` - Proxy para user-service
- `GET /orders` - Proxy para order-service
- `GET /orders/<id>` - Proxy para order-service
- `GET /users/<id>/complete` - **Agregação** de dados

#### **User Service** (Porta 5001 - Interna)

- **Função**: Gerenciamento de usuários
- **Dados**: Nome, email, departamento
- **Exposição**: Apenas via gateway (não diretamente acessível externamente)

**Endpoints:**

- `GET /users` - Lista usuários
- `GET /users/<id>` - Detalhes de um usuário

#### **Order Service** (Porta 5002 - Interna)

- **Função**: Gerenciamento de pedidos
- **Dados**: Produto, valor, status, data
- **Exposição**: Apenas via gateway

**Endpoints:**

- `GET /orders` - Lista pedidos
- `GET /orders/<id>` - Detalhes de um pedido
- `GET /orders/user/<user_id>` - Pedidos de um usuário


### Padrões Implementados

#### 1. **API Gateway Pattern**

```
Cliente → Gateway → Microsserviços
```

#### 2. **Service Discovery via DNS**

```python
USER_SERVICE_URL = 'http://user-service:5001'
ORDER_SERVICE_URL = 'http://order-service:5002'
```

#### 3. **API Composition / Aggregation**

```python
# Gateway combina dados de múltiplos serviços
user_data = requests.get(f'{USER_SERVICE_URL}/users/{id}')
order_data = requests.get(f'{ORDER_SERVICE_URL}/orders/user/{id}')
combined = {**user_data, **order_data}
```

#### 4. **Health Check Aggregation**

```python
# Gateway verifica saúde de todos os serviços
health = {
    'user-service': check_service(USER_SERVICE_URL),
    'order-service': check_service(ORDER_SERVICE_URL)
}
```

### Docker Compose Orchestration

```yaml
services:
  user-service: # Microsserviço 1
  order-service: # Microsserviço 2
  gateway: # API Gateway
    depends_on:
      - user-service
      - order-service
```


## Como Executar

### Pré-requisitos

- Docker e Docker Compose instalados
- Porta 5000 disponível

### Passo 1: Navegar até o diretório

```bash
cd desafio5
```

### Passo 2: Iniciar com Docker Compose

```bash
# Método 1: Script automatizado
chmod +x run.sh test.sh cleanup.sh
./run.sh

# Método 2: Docker Compose diretamente
docker-compose up -d --build
```

O comando:

1. Constrói as imagens dos 3 serviços
2. Cria a rede `desafio5-network`
3. Inicia os microsserviços
4. Inicia o gateway (depende dos microsserviços)

### Passo 3: Verificar o status

```bash
docker-compose ps
```

Saída esperada:

```
NAME            IMAGE                    STATUS         PORTS
api-gateway     desafio5-gateway         Up             0.0.0.0:5000->5000/tcp
user-service    desafio5-user-service    Up (healthy)
order-service   desafio5-order-service   Up (healthy)
```

### Passo 4: Testar o sistema

#### Health Check:

```bash
curl http://localhost:5000/health
```

#### Listar usuários (via gateway):

```bash
curl http://localhost:5000/users
```

#### Listar pedidos (via gateway):

```bash
curl http://localhost:5000/orders
```

#### **Agregação** - Dados completos:

```bash
curl http://localhost:5000/users/1/complete
```

#### Estatísticas:

```bash
curl http://localhost:5000/stats
```

#### Teste completo automatizado:

```bash
./test.sh
```

### Passo 5: Ver logs

```bash
# Todos os serviços
docker-compose logs -f

# Gateway apenas
docker-compose logs -f gateway

# Serviço específico
docker-compose logs -f user-service
```

### Passo 6: Parar o sistema

```bash
# Parar containers
docker-compose down

# Parar e remover tudo
./cleanup.sh
```

## Funcionamento Detalhado

### Fluxo 1: Requisição Simples (Proxy)

**Cliente solicita lista de usuários:**

```
1. Cliente
     │
     │ GET http://localhost:5000/users
     ▼
2. API Gateway
     │
     │ stats['users_requests'] += 1
     │
     │ GET http://user-service:5001/users
     ▼
3. User Service
     │
     │ Busca usuários do banco (in-memory)
     │
     │ Response: {"users": [...]}
     ▼
4. API Gateway
     │
     │ Adiciona metadados: data['via'] = 'api-gateway'
     │
     │ Response: {"users": [...], "via": "api-gateway"}
     ▼
5. Cliente recebe resposta
```

### Fluxo 2: Agregação de Dados

**Cliente solicita dados completos de um usuário:**

```
1. Cliente
     │
     │ GET http://localhost:5000/users/1/complete
     ▼
2. API Gateway
     │
     ├─► GET http://user-service:5001/users/1
     │   User Service responde: {"user": {...}}
     │
     └─► GET http://order-service:5002/orders/user/1
         Order Service responde: {"orders": [...], "total": 2625.00}
     │
     │ Gateway agrega os dados:
     │
     │ {
     │   "user": {...},
     │   "orders_summary": {
     │     "total_orders": 3,
     │     "total_spent": 2625.00,
     │     "orders": [...]
     │   }
     │ }
     ▼
3. Cliente recebe dados agregados em uma única resposta
```

**Benefício:** Cliente faz 1 requisição em vez de 2!

### Fluxo 3: Health Check Agregado

```
1. Cliente → GET /health → Gateway
2. Gateway verifica user-service → GET /health
3. Gateway verifica order-service → GET /health
4. Gateway retorna status agregado:
   {
     "gateway": "healthy",
     "services": {
       "user-service": "healthy",
       "order-service": "healthy"
     }
   }
```

## Exemplos de Resposta

### GET /health

```json
{
  "gateway": "healthy",
  "overall_status": "healthy",
  "services": {
    "user-service": "healthy",
    "order-service": "healthy"
  },
  "timestamp": "2025-11-23T10:00:00"
}
```

### GET /users (via gateway)

```json
{
  "service": "user-service",
  "count": 5,
  "users": [
    {
      "id": 1,
      "name": "Alice Silva",
      "email": "alice@email.com",
      "department": "Engineering"
    }
  ],
  "via": "api-gateway"
}
```

### GET /users/1/complete (agregação)

```json
{
  "via": "api-gateway",
  "aggregated_from": ["user-service", "order-service"],
  "user": {
    "service": "user-service",
    "user": {
      "id": 1,
      "name": "Alice Silva",
      "email": "alice@email.com",
      "department": "Engineering"
    }
  },
  "orders_summary": {
    "total_orders": 3,
    "total_spent": 2625.0,
    "orders": [
      { "id": 1, "product": "Laptop", "amount": 2500.0 },
      { "id": 2, "product": "Mouse", "amount": 50.0 },
      { "id": 7, "product": "USB Hub", "amount": 75.0 }
    ]
  },
  "timestamp": "2025-11-23T10:00:00"
}
```

### GET /stats

```json
{
  "gateway": "api-gateway",
  "statistics": {
    "total_requests": 42,
    "users_requests": 18,
    "orders_requests": 15,
    "errors": 0
  },
  "timestamp": "2025-11-23T10:00:00"
}
```

## Testes e Validação

### Teste 1: Gateway como ponto único de entrada

```bash
# Todas as requisições através do gateway
curl http://localhost:5000/users
curl http://localhost:5000/orders

# Microsserviços NÃO são acessíveis diretamente do host
# (portas 5001 e 5002 não são expostas no docker-compose.yml)
```

### Teste 2: Agregação de dados

```bash
# Uma requisição retorna dados de dois serviços
curl http://localhost:5000/users/1/complete | jq '.'

# Verifique que contém dados de user + orders
```

### Teste 3: Health check agregado

```bash
# Gateway verifica saúde de todos os serviços
curl http://localhost:5000/health

# Deve mostrar status de user-service e order-service
```

### Teste 4: Resiliência

```bash
# Para o user-service
docker-compose stop user-service

# Gateway deve retornar erro apropriado
curl http://localhost:5000/users
# {"error": "Failed to reach user service"}

# Health check deve mostrar degradação
curl http://localhost:5000/health
# {"overall_status": "degraded", "services": {"user-service": "unreachable"}}

# Reinicia o serviço
docker-compose start user-service

# Tudo volta a funcionar
curl http://localhost:5000/users
```

### Teste 5: Estatísticas

```bash
# Faz várias requisições
for i in {1..10}; do
    curl -s http://localhost:5000/users > /dev/null
    curl -s http://localhost:5000/orders > /dev/null
done

# Verifica estatísticas
curl http://localhost:5000/stats
# Deve mostrar contadores atualizados
```
