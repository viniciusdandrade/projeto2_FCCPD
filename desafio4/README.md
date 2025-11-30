# Desafio 4 - Microsserviços Independentes

## Descrição

Este desafio implementa dois microsserviços independentes que se comunicam via HTTP. O **Service A** fornece dados de usuários, enquanto o **Service B** consome esses dados e os enriquece com informações adicionais, demonstrando o padrão de arquitetura de microsserviços.

## Arquitetura

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

