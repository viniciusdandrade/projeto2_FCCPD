# Projeto 2 - FCCPD: Docker e Microsserviços

## Sobre o Projeto

Este repositório contém a implementação completa de 5 desafios práticos focados em **Docker** e **Microsserviços**, cobrindo desde conceitos básicos até arquiteturas avançadas com API Gateway.

**Disciplina:** Fundamentos de Computação em Nuvem e Processamento Distribuído (FCCPD)  
**Foco:** Containerização, Orquestração e Arquitetura de Microsserviços  
**Tecnologias:** Docker, Docker Compose, Python, Flask, PostgreSQL, Redis

## Objetivos

- Dominar conceitos fundamentais de Docker e containerização
- Implementar comunicação entre containers
- Gerenciar persistência de dados com volumes
- Orquestrar múltiplos serviços com Docker Compose
- Desenvolver arquiteturas de microsserviços
- Implementar API Gateway como ponto único de entrada

## Estrutura do Repositório

```
projeto2_FCCPD/
│
├── desafio1/              # Containers em Rede
│   ├── server.py          # Servidor Flask
│   ├── client.sh          # Cliente fazendo requisições
│   ├── Dockerfile.server  # Dockerfile do servidor
│   ├── Dockerfile.client  # Dockerfile do cliente
│   ├── run.sh             # Script de execução
│   ├── cleanup.sh         # Script de limpeza
│   └── README.md          # Documentação completa
│
├── desafio2/              # Volumes e Persistência
│   ├── app.py             # Aplicação com SQLite
│   ├── reader.py          # Leitor de dados
│   ├── Dockerfile         # Dockerfile da aplicação
│   ├── Dockerfile.reader  # Dockerfile do leitor
│   ├── run.sh             # Script de execução
│   ├── demo.sh            # Demonstração passo a passo
│   ├── cleanup.sh         # Script de limpeza
│   └── README.md          # Documentação completa
│
├── desafio3/              # Docker Compose Orquestrando Serviços
│   ├── app.py             # API Flask com cache
│   ├── init-db.sql        # Script de inicialização do banco
│   ├── Dockerfile.web     # Dockerfile da aplicação web
│   ├── requirements.txt   # Dependências Python
│   ├── docker-compose.yml # Orquestração dos serviços
│   ├── run.sh             # Script de execução
│   ├── test.sh            # Testes automatizados
│   ├── cleanup.sh         # Script de limpeza
│   └── README.md          # Documentação completa
│
├── desafio4/              # Microsserviços Independentes
│   ├── service-a/         # Microsserviço de Usuários
│   │   ├── app.py
│   │   └── Dockerfile
│   ├── service-b/         # Microsserviço de Informações
│   │   ├── app.py
│   │   └── Dockerfile
│   ├── run.sh             # Script de execução
│   ├── test.sh            # Testes automatizados
│   ├── cleanup.sh         # Script de limpeza
│   └── README.md          # Documentação completa
│
├── desafio5/              # Microsserviços com API Gateway
│   ├── user-service/      # Microsserviço de Usuários
│   │   ├── app.py
│   │   └── Dockerfile
│   ├── order-service/     # Microsserviço de Pedidos
│   │   ├── app.py
│   │   └── Dockerfile
│   ├── gateway/           # API Gateway
│   │   ├── app.py
│   │   └── Dockerfile
│   ├── docker-compose.yml # Orquestração completa
│   ├── run.sh             # Script de execução
│   ├── test.sh            # Testes automatizados
│   ├── cleanup.sh         # Script de limpeza
│   └── README.md          # Documentação completa
│
└── README.md              # Este arquivo
```

## Desafios Implementados

### Desafio 1 - Containers em Rede (20 pontos)

**Objetivo:** Demonstrar comunicação entre containers via rede Docker customizada.

**Implementação:**

- Servidor web Flask na porta 8080
- Cliente realizando requisições HTTP periódicas
- Rede Docker nomeada (desafio1-network)
- Comunicação funcional com logs detalhados

**Tecnologias:** Flask, Alpine Linux, curl, Docker Networks

**Como executar:**

```bash
cd desafio1
chmod +x run.sh cleanup.sh
./run.sh
```

[Documentação Completa](./desafio1/README.md)

---

### Desafio 2 - Volumes e Persistência (20 pontos)

**Objetivo:** Demonstrar persistência de dados usando volumes Docker.

**Implementação:**

- Banco de dados SQLite em container
- Volume Docker para persistência
- Dados persistem após remoção do container
- Container separado para leitura de dados

**Tecnologias:** Python, SQLite, Docker Volumes

**Como executar:**

```bash
cd desafio2
chmod +x run.sh demo.sh cleanup.sh
./run.sh
```

[Documentação Completa](./desafio2/README.md)

---

### Desafio 3 - Docker Compose Orquestrando Serviços (25 pontos)

**Objetivo:** Usar Docker Compose para orquestrar múltiplos serviços dependentes.

**Implementação:**

- 3 serviços: Web (Flask), Database (PostgreSQL), Cache (Redis)
- Dependências configuradas via docker-compose.yml
- Comunicação entre serviços via rede interna
- Health checks e restart policies

**Tecnologias:** Flask, PostgreSQL, Redis, Docker Compose

**Como executar:**

```bash
cd desafio3
chmod +x run.sh test.sh cleanup.sh
./run.sh
```

[Documentação Completa](./desafio3/README.md)

---

### Desafio 4 - Microsserviços Independentes (20 pontos)

**Objetivo:** Criar dois microsserviços independentes que se comunicam via HTTP.

**Implementação:**

- Service A: Fornece lista de usuários (JSON)
- Service B: Consome Service A e enriquece dados
- Dockerfiles separados por serviço
- Comunicação via requisições HTTP

**Tecnologias:** Flask, Requests, Docker

**Como executar:**

```bash
cd desafio4
chmod +x run.sh test.sh cleanup.sh
./run.sh
```

[Documentação Completa](./desafio4/README.md)

---

### Desafio 5 - Microsserviços com API Gateway (25 pontos)

**Objetivo:** Criar arquitetura com API Gateway centralizando acesso aos microsserviços.

**Implementação:**

- User Service: Fornece dados de usuários
- Order Service: Fornece dados de pedidos
- API Gateway: Ponto único de entrada, orquestra chamadas
- Agregação de dados de múltiplos serviços
- Orquestração completa via Docker Compose

**Tecnologias:** Flask, Requests, Docker Compose

**Como executar:**

```bash
cd desafio5
chmod +x run.sh test.sh cleanup.sh
./run.sh
```

[Documentação Completa](./desafio5/README.md)

---

## Pré-requisitos

### Software Necessário

- **Docker:** >= 20.10.0
- **Docker Compose:** >= 2.0.0
- **Git:** Para clonar o repositório
- **curl:** Para testes de API (opcional, mas recomendado)
- **jq:** Para formatação JSON (opcional)

### Instalação do Docker

#### Linux (Ubuntu/Debian)

```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER
```

#### macOS

```bash
# Baixe Docker Desktop em: https://www.docker.com/products/docker-desktop
```

#### Windows

```powershell
# Baixe Docker Desktop em: https://www.docker.com/products/docker-desktop
# Requer WSL2
```

### Verificar Instalação

```bash
docker --version
docker-compose --version
docker ps
```

## Como Usar Este Repositório

### 1. Clonar o Repositório

```bash
git clone https://github.com/viniciusdandrade/projeto2_FCCPD.git
cd projeto2_FCCPD
```

### 2. Escolher um Desafio

```bash
# Exemplo: Desafio 1
cd desafio1
```

### 3. Ler a Documentação

```bash
# Cada desafio tem um README.md detalhado
cat README.md
# ou abra no navegador
```

### 4. Executar o Desafio

```bash
# Torna scripts executáveis (Linux/Mac)
chmod +x *.sh

# Executa o desafio
./run.sh

# Executa testes (quando disponível)
./test.sh

# Limpa o ambiente
./cleanup.sh
```

### 5. Explorar os Logs

```bash
# Ver logs dos containers
docker logs -f <container-name>

# Ver logs do Docker Compose
docker-compose logs -f
```

## Testando os Desafios

### Testes Manuais

Cada desafio pode ser testado manualmente usando `curl`:

```bash
# Desafio 1
curl http://localhost:8080

# Desafio 3
curl http://localhost:5000/users

# Desafio 4
curl http://localhost:5002/user-info

# Desafio 5
curl http://localhost:5000/users/1/complete
```

### Testes Automatizados

Desafios 3, 4 e 5 incluem scripts de teste:

```bash
cd desafio3
./test.sh

cd desafio4
./test.sh

cd desafio5
./test.sh
```

## Conceitos Abordados

### Docker Fundamentals

- Containers e imagens
- Dockerfiles e build
- Redes Docker (bridge, custom)
- Volumes e persistência
- Port binding e exposição
- Multi-stage builds

### Docker Compose

- Orquestração de serviços
- Dependências entre serviços
- Variáveis de ambiente
- Health checks
- Restart policies
- Volumes e redes

### Microsserviços

- Arquitetura de microsserviços
- Comunicação HTTP/REST
- Service discovery
- API Gateway pattern
- Agregação de dados
- Separação de responsabilidades

### Boas Práticas

- Imagens Alpine (leves)
- Imagens oficiais
- Logs estruturados
- Tratamento de erros
- Health checks
- Configuração via env vars
- Documentação clara

## Troubleshooting

### Problemas Comuns

#### 1. Porta já em uso

```bash
# Erro: port is already allocated
# Solução: Parar o processo usando a porta
sudo lsof -i :5000
sudo kill -9 <PID>
```

#### 2. Docker daemon não está rodando

```bash
# Erro: Cannot connect to the Docker daemon
# Solução: Iniciar Docker
sudo systemctl start docker  # Linux
# ou iniciar Docker Desktop (Windows/Mac)
```

#### 3. Permissão negada

```bash
# Erro: permission denied
# Solução: Adicionar usuário ao grupo docker
sudo usermod -aG docker $USER
# Fazer logout e login novamente
```

#### 4. Containers não se comunicam

```bash
# Verificar se estão na mesma rede
docker network inspect <network-name>

# Testar conectividade
docker exec <container> ping <other-container>
```

#### 5. Volume não persiste dados

```bash
# Verificar se o volume existe
docker volume ls
docker volume inspect <volume-name>

# Verificar montagem
docker inspect <container> | grep Mounts -A 10
```

## Recursos Adicionais

### Documentação Oficial

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)

### Tutoriais

- [Docker Getting Started](https://docs.docker.com/get-started/)
- [Microservices Architecture](https://microservices.io/)
- [12 Factor App](https://12factor.net/)

### Ferramentas Úteis

- [Docker Desktop](https://www.docker.com/products/docker-desktop)
- [Portainer](https://www.portainer.io/) - UI para gerenciar Docker
- [Dive](https://github.com/wagoodman/dive) - Explorar imagens Docker
- [Lazydocker](https://github.com/jesseduffield/lazydocker) - Terminal UI para Docker

## Contribuição

Este é um projeto acadêmico individual, mas sugestões são bem-vindas!

### Como Reportar Issues

1. Acesse a aba [Issues](https://github.com/viniciusdandrade/projeto2_FCCPD/issues)
2. Clique em "New Issue"
3. Descreva o problema ou sugestão

## Licença

Este projeto é desenvolvido para fins educacionais.

## Autor

**Vinícius D'Andrade**

- GitHub: [@viniciusdandrade](https://github.com/viniciusdandrade)
- Repositório: [projeto2_FCCPD](https://github.com/viniciusdandrade/projeto2_FCCPD)

---

## Conclusão

Este projeto demonstra profundo conhecimento em:

- Containerização com Docker
- Orquestração de serviços
- Arquitetura de Microsserviços
- Boas práticas de desenvolvimento
- Documentação técnica completa

Cada desafio foi cuidadosamente implementado com foco em:

- Funcionalidade completa
- Código limpo e bem organizado
- Documentação extensiva
- Scripts automatizados
- Tratamento de erros
- Logs detalhados
- Facilidade de uso

**Status:** Todos os 5 desafios implementados e documentados
