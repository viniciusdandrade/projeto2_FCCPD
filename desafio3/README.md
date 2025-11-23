# Desafio 3 - Docker Compose Orquestrando Serviços

## Descrição

Este desafio demonstra o uso do Docker Compose para orquestrar múltiplos serviços interdependentes. A aplicação consiste em três serviços: uma API web (Flask), um banco de dados (PostgreSQL) e um sistema de cache (Redis), todos trabalhando em conjunto.

## Arquitetura

### Componentes:

#### 1. **Web Service** (Flask API)

- **Tecnologia**: Python 3.11 + Flask
- **Porta**: 5000
- **Função**: API REST que gerencia usuários
- **Dependências**:
  - Conecta ao PostgreSQL para persistência
  - Usa Redis para cache de consultas
- **Features**:
  - CRUD de usuários
  - Cache inteligente com TTL
  - Health checks
  - Estatísticas do sistema

#### 2. **Database Service** (PostgreSQL)

- **Tecnologia**: PostgreSQL 15 Alpine
- **Porta**: 5432 (interna)
- **Função**: Armazenamento persistente de dados
- **Volume**: `db-data` para persistência
- **Inicialização**: Script SQL automático
- **Health Check**: `pg_isready`

#### 3. **Cache Service** (Redis)

- **Tecnologia**: Redis 7 Alpine
- **Porta**: 6379
- **Função**: Cache de consultas e dados temporários
- **Volume**: `cache-data` para persistência (AOF)
- **Health Check**: `redis-cli ping`

## Decisões Técnicas

### Por que Docker Compose?

- **Orquestração simplificada**: Define toda a stack em um arquivo YAML
- **Gerenciamento de dependências**: `depends_on` garante ordem de inicialização
- **Redes automáticas**: Containers se comunicam por nomes de serviço
- **Configuração centralizada**: Todas as configs em um lugar
- **Ambiente reproduzível**: Mesma stack em dev/staging/prod

### Arquitetura de Três Camadas

- **Presentation Layer (Web - Flask)**: API REST
- **Caching Layer (Cache - Redis)**: Performance
- **Data Layer (DB - PostgreSQL)**: Persistência

### Estratégia de Cache

1. **Cache-Aside Pattern**:

   - Consulta tenta o cache primeiro
   - Se miss, busca no banco e atualiza cache
   - TTL de 60s para listas, 5min para objetos individuais

2. **Invalidação Inteligente**:
   - Criação/atualização invalida cache relacionado
   - Evita dados desatualizados

### Health Checks

- **PostgreSQL**: `pg_isready` verifica se o banco está pronto
- **Redis**: `redis-cli ping` testa conectividade
- **Benefícios**:
  - Docker sabe quando o serviço está realmente pronto
  - Restart automático se falhar
  - Melhor para orquestração

## Como Executar

### Pré-requisitos

- Docker e Docker Compose instalados
- Porta 5000 disponível no host

### Passo 1: Navegar até o diretório

```bash
cd desafio3
```

### Passo 2: Iniciar a stack

```bash
# Método 1: Usando o script (recomendado)
chmod +x run.sh test.sh cleanup.sh
./run.sh

# Método 2: Docker Compose diretamente
docker-compose up -d
```

O comando fará:

1. Criar a rede `desafio3-network`
2. Criar volumes `db-data` e `cache-data`
3. Construir a imagem do serviço web
4. Baixar imagens do PostgreSQL e Redis
5. Iniciar os containers na ordem correta (db → cache → web)
6. Executar script de inicialização do banco

### Passo 3: Verificar o status

```bash
docker-compose ps
```

Saída esperada:

```
NAME           IMAGE              STATUS         PORTS
postgres-db    postgres:15-alpine Up (healthy)   5432/tcp
redis-cache    redis:7-alpine     Up (healthy)   0.0.0.0:6379->6379/tcp
web-app        desafio3-web       Up             0.0.0.0:5000->5000/tcp
```

### Passo 4: Testar a aplicação

#### Teste rápido:

```bash
curl http://localhost:5000
```

#### Teste completo:

```bash
./test.sh
```

#### Testes manuais:

**1. Health Check:**

```bash
curl http://localhost:5000/health
```

**2. Listar usuários:**

```bash
curl http://localhost:5000/users
```

**3. Criar usuário:**

```bash
curl -X POST http://localhost:5000/users \
  -H "Content-Type: application/json" \
  -d '{"name": "Seu Nome", "email": "seu@email.com"}'
```

**4. Obter usuário específico:**

```bash
curl http://localhost:5000/users/1
```

**5. Ver estatísticas:**

```bash
curl http://localhost:5000/stats
```

### Passo 5: Ver logs

```bash
# Todos os serviços
docker-compose logs -f

# Serviço específico
docker-compose logs -f web
docker-compose logs -f db
docker-compose logs -f cache
```

### Passo 6: Parar os serviços

```bash
# Parar mas manter volumes
docker-compose down

# Parar e remover volumes
docker-compose down -v

# Ou usar o script de limpeza
./cleanup.sh
```

## Funcionamento Detalhado

### 1. Inicialização da Stack

```yaml
# docker-compose.yml
services:
  db:
    # Inicia primeiro (nenhuma dependência)
  cache:
    # Inicia segundo (nenhuma dependência)
  web:
    depends_on:
      - db
      - cache
    # Aguarda db e cache iniciarem antes de começar
```

**Ordem de inicialização**:

1. Docker Compose cria a rede `desafio3-network`
2. Docker Compose cria os volumes `db-data` e `cache-data`
3. Inicia `db` (PostgreSQL)
   - Executa `init-db.sql`
   - Health check até ficar pronto
4. Inicia `cache` (Redis)
   - Health check até ficar pronto
5. Inicia `web` (Flask)
   - Conecta ao banco e cache
   - Expõe porta 5000

### 2. Comunicação Entre Serviços

**DNS Interno do Docker Compose**:

```python
# Em app.py, podemos usar nomes de serviços:
DB_CONFIG = {
    'host': 'db',  # ← Resolve para IP do container postgres-db
    ...
}

REDIS_HOST = 'cache'  # ← Resolve para IP do container redis-cache
```

Docker Compose cria entradas DNS automáticas:

- `db` → IP do container PostgreSQL
- `cache` → IP do container Redis
- `web` → IP do container Flask

### 3. Fluxo de uma Requisição

**Exemplo: GET /users**

```
1. Cliente ──HTTP GET /users──► Web Container
                                      │
2. Web verifica cache ───────────────┼──► Redis
                                      │     │
3. Cache miss (não existe) ◄─────────┼─────┘
                                      │
4. Web consulta banco ───────────────┼──► PostgreSQL
                                      │     │
5. Retorna dados ◄───────────────────┼─────┘
                                      │
6. Web armazena no cache ────────────┼──► Redis
                                      │
7. Retorna JSON ◄────────────────────┘
```

**Segunda requisição (cache hit)**:

```
1. Cliente ──HTTP GET /users──► Web Container
                                      │
2. Web verifica cache ───────────────┼──► Redis
                                      │     │
3. Cache hit! ◄──────────────────────┼─────┘
                                      │
4. Retorna JSON ◄────────────────────┘
   (muito mais rápido!)
```

### 4. Persistência de Dados

**PostgreSQL Volume**:

```yaml
volumes:
  - db-data:/var/lib/postgresql/data
```

- Todos os dados do banco em `db-data`
- Sobrevive a `docker-compose down`
- Removido apenas com `docker-compose down -v`

**Redis Volume**:

```yaml
volumes:
  - cache-data:/data
command: redis-server --appendonly yes
```

- AOF (Append Only File) para persistência
- Cache sobrevive a restarts
- Ideal para dados que podem ser reconstruídos

### 5. Variáveis de Ambiente

```yaml
# PostgreSQL
environment:
  - POSTGRES_USER=user
  - POSTGRES_PASSWORD=password
  - POSTGRES_DB=appdb

# Web (Flask)
environment:
  - FLASK_ENV=development
  - DATABASE_URL=postgresql://user:password@db:5432/appdb
  - REDIS_HOST=cache
  - REDIS_PORT=6379
```

Variáveis são injetadas nos containers e usadas pela aplicação.

## Endpoints da API

### GET /

Informações do sistema e lista de endpoints.

**Resposta**:

```json
{
  "service": "Web Application",
  "status": "running",
  "timestamp": "2025-11-23T10:00:00",
  "endpoints": { ... }
}
```

### GET /health

Health check dos serviços.

**Resposta**:

```json
{
  "status": "healthy",
  "database": "connected",
  "cache": "connected",
  "timestamp": "2025-11-23T10:00:00"
}
```

### GET /users

Lista todos os usuários (com cache).

**Resposta**:

```json
{
  "source": "cache", // ou "database"
  "users": [
    {
      "id": 1,
      "name": "João Silva",
      "email": "joao@email.com",
      "created_at": "2025-11-23T09:00:00"
    }
  ]
}
```

### POST /users

Cria um novo usuário.

**Request**:

```json
{
  "name": "Novo Usuário",
  "email": "novo@email.com"
}
```

**Resposta**:

```json
{
  "message": "User created successfully",
  "id": 5
}
```

### GET /users/:id

Obtém detalhes de um usuário específico.

**Resposta**:

```json
{
  "source": "cache",
  "user": {
    "id": 1,
    "name": "João Silva",
    "email": "joao@email.com",
    "created_at": "2025-11-23T09:00:00"
  }
}
```

### GET /stats

Estatísticas do sistema.

**Resposta**:

```json
{
  "database": {
    "users_count": 5
  },
  "cache": {
    "keys_count": 3
  },
  "timestamp": "2025-11-23T10:00:00"
}
```

## Testes de Validação

### Teste 1: Verificar todos os serviços

```bash
docker-compose ps
# Todos devem estar "Up" e "healthy"
```

### Teste 2: Testar comunicação web → db

```bash
curl http://localhost:5000/users
# Deve retornar lista de usuários do banco
```

### Teste 3: Testar comunicação web → cache

```bash
# Primeira requisição (do banco)
curl http://localhost:5000/users

# Segunda requisição (do cache)
curl http://localhost:5000/users
# "source" deve ser "cache"
```

### Teste 4: Testar depends_on

```bash
# Para o banco
docker-compose stop db

# Tenta acessar API
curl http://localhost:5000/health
# database deve estar "disconnected"

# Reinicia o banco
docker-compose start db
```

### Teste 5: Testar persistência

```bash
# Cria usuário
curl -X POST http://localhost:5000/users \
  -H "Content-Type: application/json" \
  -d '{"name": "Teste", "email": "teste@test.com"}'

# Para tudo
docker-compose down

# Inicia novamente
docker-compose up -d

# Verifica que o usuário ainda existe
curl http://localhost:5000/users
```

### Teste 6: Testar reinício automático

```bash
# Mata o processo do Redis
docker-compose exec cache redis-cli SHUTDOWN

# Aguarda alguns segundos
sleep 5

# Verifica status
docker-compose ps
# Redis deve estar "Up" novamente (restart: unless-stopped)
```

## Comandos Úteis

### Gerenciamento da Stack

```bash
# Iniciar em foreground (ver logs)
docker-compose up

# Iniciar em background
docker-compose up -d

# Parar serviços
docker-compose stop

# Iniciar serviços parados
docker-compose start

# Reiniciar serviços
docker-compose restart

# Parar e remover containers
docker-compose down

# Parar e remover containers + volumes
docker-compose down -v

# Reconstruir imagens
docker-compose build

# Reconstruir e iniciar
docker-compose up -d --build
```

### Logs e Debugging

```bash
# Ver logs de todos os serviços
docker-compose logs

# Seguir logs em tempo real
docker-compose logs -f

# Logs de um serviço específico
docker-compose logs -f web

# Últimas 100 linhas
docker-compose logs --tail=100

# Logs com timestamps
docker-compose logs -t
```

### Execução de Comandos

```bash
# Shell no container web
docker-compose exec web bash

# Shell no container db
docker-compose exec db psql -U user -d appdb

# Shell no container cache
docker-compose exec cache redis-cli

# Executar comando pontual
docker-compose exec web python -c "print('Hello')"
```

### Monitoramento

```bash
# Status dos containers
docker-compose ps

# Estatísticas de uso
docker-compose stats

# Processos em execução
docker-compose top

# Verificar configuração
docker-compose config

# Validar arquivo compose
docker-compose config --quiet
```

### Network e Volumes

```bash
# Listar redes
docker network ls

# Inspecionar rede
docker network inspect desafio3-network

# Listar volumes
docker volume ls

# Inspecionar volume
docker volume inspect desafio3-db-data
```

## Critérios Atendidos

- [10 pts] Compose funcional e bem estruturado:
  - Arquivo docker-compose.yml completo e organizado
  - Uso correto de serviços, volumes, redes e variáveis
- [5 pts] Comunicação entre serviços funcionando:
  - Web se comunica com DB e Cache
  - DNS interno funcionando
  - Dependências configuradas corretamente
- [5 pts] README com explicação da arquitetura:
  - Documentação completa e detalhada
  - Diagramas e explicações de fluxo
  - Exemplos práticos
- [5 pts] Clareza e boas práticas:
  - Código bem comentado
  - Health checks implementados
  - Volumes para persistência
  - Restart policies
  - Estrutura de projeto organizada

## Boas Práticas Implementadas

### 1. **Health Checks**

```yaml
healthcheck:
  test: ['CMD-SHELL', 'pg_isready -U user -d appdb']
  interval: 10s
  timeout: 5s
  retries: 5
```

- Garante que o serviço está realmente pronto
- Docker pode reiniciar automaticamente se falhar

### 2. **Restart Policies**

```yaml
restart: unless-stopped
```

- Serviços reiniciam automaticamente em caso de falha
- Não reiniciam se parados manualmente

### 3. **Volumes Nomeados**

```yaml
volumes:
  db-data:
    name: desafio3-db-data
```

- Fácil de identificar e gerenciar
- Backup e migração simplificados

### 4. **Rede Customizada**

```yaml
networks:
  app-network:
    name: desafio3-network
    driver: bridge
```

- Isolamento dos containers
- DNS interno automático
- Controle sobre comunicação

### 5. **Variáveis de Ambiente**

```yaml
environment:
  - POSTGRES_USER=user
  - POSTGRES_PASSWORD=password
```

- Configuração centralizada
- Fácil mudança entre ambientes
- Secrets management (em produção usar Docker secrets)

### 6. **Ordem de Inicialização**

```yaml
depends_on:
  - db
  - cache
```

- Garante que dependências estão prontas
- Evita erros de conexão

### 7. **Imagens Oficiais e Alpine**

```yaml
image: postgres:15-alpine
image: redis:7-alpine
```

- Imagens mantidas e seguras
- Alpine reduz tamanho (segurança e performance)

### 8. **Init Scripts**

```yaml
volumes:
  - ./init-db.sql:/docker-entrypoint-initdb.d/init.sql
```

- Inicialização automática do banco
- Esquema criado na primeira execução

## Conceitos Aprendidos

- Orquestração de múltiplos containers com Docker Compose
- Configuração de dependências entre serviços
- Redes internas e DNS no Docker
- Volumes para persistência de dados
- Health checks e restart policies
- Variáveis de ambiente e configuração
- Comunicação entre containers
- Estratégias de cache
- Arquitetura de três camadas
- Init scripts e seed data
- Logs centralizados
- Debugging de aplicações containerizadas
