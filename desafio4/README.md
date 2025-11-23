# Desafio 4 - Microsserviços Independentes

## Descrição

Este desafio implementa dois microsserviços independentes que se comunicam via HTTP. O **Service A** fornece dados de usuários, enquanto o **Service B** consome esses dados e os enriquece com informações adicionais, demonstrando o padrão de arquitetura de microsserviços.

## Arquitetura

```
┌──────────────────────────────────────────────────┐
│          Rede: microservices-network              │
│                                                   │
│   ┌─────────────┐           ┌─────────────┐     │
│   │  Service A  │           │  Service B  │     │
│   │   (Users)   │◄──────────┤ (User Info) │     │
│   │   :5001     │  HTTP GET │   :5002     │     │
│   └──────┬──────┘           └──────┬──────┘     │
│          │                         │             │
└──────────┼─────────────────────────┼─────────────┘
           │                         │
      Host:5001                 Host:5002
```

### Componentes:

#### **Service A - User Service** (Porta 5001)

- **Função**: Provedor de dados de usuários
- **Responsabilidade**: Gerenciar e fornecer informações básicas de usuários
- **Tecnologia**: Flask (Python)
- **Dados**: Base de usuários em memória

**Endpoints:**

- `GET /` - Informações do serviço
- `GET /health` - Health check
- `GET /users` - Lista todos os usuários
- `GET /users/<id>` - Detalhes de um usuário
- `GET /users/active` - Usuários ativos
- `GET /users/inactive` - Usuários inativos

#### **Service B - User Info Service** (Porta 5002)

- **Função**: Consumidor e enriquecedor de dados
- **Responsabilidade**: Consumir dados do Service A e adicionar informações processadas
- **Tecnologia**: Flask (Python) + Requests
- **Dependência**: Service A

**Endpoints:**

- `GET /` - Informações do serviço
- `GET /health` - Health check (verifica conexão com Service A)
- `GET /user-info` - Informações enriquecidas de todos os usuários
- `GET /user-info/<id>` - Informações enriquecidas de um usuário
- `GET /user-summary` - Resumo estatístico dos usuários

## Decisões Técnicas

### Arquitetura de Microsserviços

**Por que dividir em dois serviços?**

1. **Separação de Responsabilidades**:

   - Service A: Fonte de dados (Single Source of Truth)
   - Service B: Lógica de negócio e apresentação

2. **Escalabilidade Independente**:

   - Cada serviço pode escalar conforme sua demanda
   - Service A pode ter cache próprio
   - Service B pode ter múltiplas instâncias

3. **Desenvolvimento Independente**:
   - Times diferentes podem trabalhar em cada serviço
   - Deploy independente
   - Tecnologias diferentes se necessário

### Comunicação HTTP/REST

**Por que HTTP em vez de mensageria?**

- ✅ Simplicidade de implementação
- ✅ Síncrono e fácil de debugar
- ✅ Padrão bem estabelecido (REST)
- ✅ Ideal para operações de leitura

**Quando usar mensageria:**

- Operações assíncronas
- Event-driven architecture
- Alto volume de mensagens
- Necessidade de fila e retry

### Isolamento via Docker

Cada microsserviço tem:

- **Dockerfile próprio**: Build independente
- **Container próprio**: Isolamento de recursos
- **Porta própria**: Sem conflitos
- **Imagem própria**: Versionamento independente

### Enriquecimento de Dados

Service B adiciona:

- Cálculo de tempo como membro
- Formatação de status
- Estatísticas agregadas
- Resumos personalizados

Isso demonstra **Separation of Concerns**:

- Service A: Dados brutos
- Service B: Dados processados

## Como Executar

### Pré-requisitos

- Docker instalado
- Portas 5001 e 5002 disponíveis

### Método 1: Script Automatizado

```bash
cd desafio4

# Torna scripts executáveis (Linux/Mac)
chmod +x run.sh test.sh cleanup.sh

# Executa
./run.sh
```

### Método 2: Manual

#### Passo 1: Criar a rede

```bash
docker network create microservices-network
```

#### Passo 2: Construir e iniciar Service A

```bash
cd service-a
docker build -t service-a .
docker run -d \
  --name service-a \
  --network microservices-network \
  -p 5001:5001 \
  service-a
cd ..
```

#### Passo 3: Construir e iniciar Service B

```bash
cd service-b
docker build -t service-b .
docker run -d \
  --name service-b \
  --network microservices-network \
  -p 5002:5002 \
  -e USER_SERVICE_URL=http://service-a:5001 \
  service-b
cd ..
```

#### Passo 4: Verificar

```bash
docker ps
curl http://localhost:5001/health
curl http://localhost:5002/health
```

## Funcionamento Detalhado

### Fluxo de Comunicação

**Cenário: Cliente solicita informações enriquecidas de usuários**

```
1. Cliente
     │
     │ HTTP GET /user-info
     ▼
2. Service B (User Info)
     │
     │ Precisa de dados de usuários
     │
     │ HTTP GET http://service-a:5001/users
     ▼
3. Service A (Users)
     │
     │ Retorna dados brutos
     │
     │ Response: {"users": [...]}
     ▼
4. Service B
     │
     │ Enriquece dados:
     │  - Calcula tempo como membro
     │  - Formata status
     │  - Adiciona resumos
     │
     │ Response: {"users": [...enriched...]}
     ▼
5. Cliente recebe dados enriquecidos
```

### Exemplo de Transformação de Dados

**Dados do Service A** (brutos):

```json
{
  "id": 1,
  "name": "Alice Silva",
  "email": "alice@email.com",
  "role": "Developer",
  "active": true,
  "joined_date": "2023-01-15"
}
```

**Dados do Service B** (enriquecidos):

```json
{
  "id": 1,
  "name": "Alice Silva",
  "email": "alice@email.com",
  "role": "Developer",
  "active": true,
  "joined_date": "2023-01-15",
  "enriched_info": {
    "days_since_joined": 678,
    "years_active": 1,
    "months_active": 10,
    "status_text": "Ativo",
    "profile_summary": "Alice Silva - Developer (Ativo)",
    "member_since": "Alice Silva é membro desde 2023-01-15 (1 anos, 10 meses)"
  }
}
```

### Comunicação entre Containers

**DNS Interno do Docker:**

```python
# No Service B:
USER_SERVICE_URL = 'http://service-a:5001'

# Docker resolve 'service-a' para o IP do container
# Exemplo: 172.18.0.2
```

**Requisição HTTP:**

```python
import requests

# Service B faz requisição para Service A
response = requests.get(f'{USER_SERVICE_URL}/users', timeout=10)
data = response.json()
users = data['users']

# Processa e enriquece os dados
enriched = [enrich_user_data(u) for u in users]
```

## Testes e Validações

### Teste 1: Verificar Service A (Standalone)

```bash
curl http://localhost:5001/users
```

Resposta esperada:

```json
{
  "service": "user-service",
  "count": 5,
  "users": [...]
}
```

### Teste 2: Verificar Service B (Consome A)

```bash
curl http://localhost:5002/user-info
```

Resposta esperada:

```json
{
  "service": "user-info-service",
  "source": "user-service",
  "count": 5,
  "users": [
    {
      "id": 1,
      "name": "Alice Silva",
      "enriched_info": {
        "profile_summary": "Alice Silva - Developer (Ativo)",
        "member_since": "Alice Silva é membro desde 2023-01-15 (1 anos, 10 meses)"
      }
    }
  ]
}
```

### Teste 3: Verificar comunicação (Health Check)

```bash
curl http://localhost:5002/health
```

Resposta esperada:

```json
{
  "status": "healthy",
  "service": "user-info-service",
  "dependencies": {
    "user-service": "connected"
  }
}
```

### Teste 4: Resumo estatístico

```bash
curl http://localhost:5002/user-summary
```

Resposta esperada:

```json
{
  "service": "user-info-service",
  "source": "user-service",
  "summary": {
    "total_users": 5,
    "active_users": 4,
    "inactive_users": 1,
    "active_percentage": 80.0,
    "roles_distribution": {
      "Developer": 2,
      "Designer": 1,
      "Manager": 1,
      "Analyst": 1
    },
    "average_years_as_member": 1.5
  }
}
```

### Teste 5: Script automatizado

```bash
./test.sh
```

Este script testa todos os endpoints e demonstra a comunicação.

## Demonstração de Logs

### Logs do Service A:

```
Microsserviço A (Users) iniciando na porta 5001...
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:5001
172.18.0.3 - - [23/Nov/2025 10:00:00] "GET /users HTTP/1.1" 200 -
172.18.0.3 - - [23/Nov/2025 10:00:05] "GET /users/1 HTTP/1.1" 200 -
```

### Logs do Service B:

```
Microsserviço B (User Info) iniciando na porta 5002...
Conectando ao User Service em: http://service-a:5001
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:5002
127.0.0.1 - - [23/Nov/2025 10:00:10] "GET /user-info HTTP/1.1" 200 -
127.0.0.1 - - [23/Nov/2025 10:00:15] "GET /user-summary HTTP/1.1" 200 -
```

## Comandos Úteis

### Gerenciamento

```bash
# Ver logs
docker logs -f service-a
docker logs -f service-b

# Reiniciar serviços
docker restart service-a service-b

# Parar serviços
docker stop service-a service-b

# Remover containers
docker rm service-a service-b

# Ver estatísticas
docker stats service-a service-b
```

### Debugging

```bash
# Executar shell no container
docker exec -it service-a bash
docker exec -it service-b bash

# Verificar rede
docker network inspect microservices-network

# Testar conectividade de dentro do Service B
docker exec service-b curl http://service-a:5001/health

# Ver variáveis de ambiente
docker exec service-b env | grep USER_SERVICE_URL
```

### Testes de Resiliência

```bash
# Parar Service A
docker stop service-a

# Tentar acessar Service B (deve retornar erro 503)
curl http://localhost:5002/user-info

# Reiniciar Service A
docker start service-a

# Service B deve voltar a funcionar
curl http://localhost:5002/user-info
```

## Critérios Atendidos

- [5 pts] Funcionamento da comunicação entre microsserviços:

  - Service B consome Service A via HTTP
  - Comunicação funcional com tratamento de erros
  - Health checks verificam conectividade

- [5 pts] Dockerfiles e isolamento corretos:

  - Dockerfile separado para cada serviço
  - Containers isolados com portas próprias
  - Rede customizada para comunicação

- [5 pts] Explicação clara da arquitetura e endpoints:

  - Documentação completa com diagramas
  - Descrição de cada endpoint
  - Exemplos de request/response

- [5 pts] Clareza e originalidade da implementação:
  - Código bem organizado e comentado
  - Enriquecimento de dados demonstra valor agregado
  - Scripts automatizados para facilitar uso

## Padrões e Boas Práticas

### 1. **Service Discovery via DNS**

```python
# Em vez de IPs hardcoded
USER_SERVICE_URL = 'http://service-a:5001'  # ✓ Usa nome do serviço
# USER_SERVICE_URL = 'http://172.18.0.2:5001'  # ✗ IP hardcoded
```

### 2. **Health Checks com Dependências**

```python
@app.route('/health')
def health():
    # Verifica não só o serviço, mas suas dependências
    user_service_status = check_dependency()
    return {'status': 'healthy', 'dependencies': {...}}
```

### 3. **Timeout em Requisições**

```python
# Sempre use timeout para evitar bloqueios infinitos
response = requests.get(url, timeout=10)
```

### 4. **Tratamento de Erros**

```python
try:
    response = requests.get(url, timeout=10)
    if response.status_code != 200:
        return error_response, 502
except requests.exceptions.RequestException:
    return error_response, 503
```

### 5. **Versionamento de APIs**

```python
# Boas práticas para produção:
@app.route('/api/v1/users')  # Versão explícita
@app.route('/api/v2/users')  # Novas versões sem quebrar clientes
```

### 6. **Configuração via Variáveis de Ambiente**

```python
USER_SERVICE_URL = os.getenv('USER_SERVICE_URL', 'http://localhost:5001')
```

### 7. **Documentação de API**

Cada serviço tem endpoint `/` com:

- Descrição do serviço
- Lista de endpoints
- Dependências
- Versão

## Considerações de Segurança

### Em Produção, considere:

1. **Autenticação entre serviços**:

   ```python
   # JWT tokens ou API keys
   headers = {'Authorization': f'Bearer {token}'}
   response = requests.get(url, headers=headers)
   ```

2. **HTTPS/TLS**:

   ```python
   # Usar HTTPS para comunicação
   USER_SERVICE_URL = 'https://service-a:5001'
   ```

3. **Rate Limiting**:

   ```python
   # Limitar requisições por segundo
   from flask_limiter import Limiter
   limiter = Limiter(app, default_limits=["100 per minute"])
   ```

4. **Circuit Breaker**:

   ```python
   # Evitar cascata de falhas
   from circuitbreaker import circuit

   @circuit(failure_threshold=5, recovery_timeout=60)
   def call_user_service():
       return requests.get(url)
   ```

5. **Service Mesh** (Avançado):
   - Istio, Linkerd
   - mTLS automático
   - Retry e timeout configuráveis
   - Observabilidade built-in

## Conceitos Aprendidos

- Arquitetura de microsserviços
- Comunicação síncrona entre serviços (HTTP/REST)
- Service discovery via DNS
- Separação de responsabilidades (Separation of Concerns)
- Health checks e monitoramento de dependências
- Tratamento de erros em sistemas distribuídos
- Isolamento de serviços com Docker
- Padrão de agregação de dados
- Configuração via variáveis de ambiente
- Resiliência e tratamento de falhas
- Versionamento de APIs
- Debugging de aplicações distribuídas

## Próximos Passos (Desafio 5)

No próximo desafio, adicionaremos um **API Gateway** que:

- Centraliza o acesso aos microsserviços
- Fornece ponto único de entrada
- Pode adicionar autenticação, rate limiting, etc.
- Simplifica o cliente (não precisa saber de múltiplos serviços)

```
Cliente → API Gateway → Service A
                      → Service B
```
