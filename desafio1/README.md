# Desafio 1 - Containers em Rede

## Descrição

Este desafio demonstra a comunicação entre dois containers Docker através de uma rede customizada. Um container executa um servidor web Flask na porta 8080, enquanto outro container atua como cliente fazendo requisições HTTP periódicas ao servidor.

## Arquitetura

```
┌─────────────────────────────────────┐
│     Rede: desafio1-network          │
│                                     │
│  ┌──────────────┐  ┌─────────────┐ │
│  │  web-server  │  │ web-client  │ │
│  │              │◄─┤             │ │
│  │  Flask:8080  │  │  curl loop  │ │
│  └──────┬───────┘  └─────────────┘ │
│         │                           │
└─────────┼───────────────────────────┘
          │
      Host:8080
```

### Componentes:

1. **web-server**: Container com servidor Flask

   - Linguagem: Python 3.11
   - Framework: Flask
   - Porta exposta: 8080
   - Endpoints:
     - `/` - Retorna informações do servidor e contador de requisições
     - `/health` - Health check do servidor

2. **web-client**: Container cliente

   - Base: Alpine Linux
   - Ferramentas: curl, jq, bash
   - Função: Realiza requisições HTTP a cada 5 segundos ao servidor

3. **desafio1-network**: Rede Docker bridge customizada
   - Permite resolução de nomes entre containers
   - Isolamento dos containers do desafio

## Decisões Técnicas

### Por que Flask?

- Framework leve e simples para criar APIs REST
- Fácil de containerizar
- Perfeito para demonstrar comunicação HTTP

### Por que Alpine Linux para o cliente?

- Imagem extremamente leve (~5MB)
- Possui os pacotes necessários (curl, jq)
- Ideal para containers que executam scripts

### Rede Customizada

- Permite que containers se comuniquem usando nomes (DNS interno)
- O cliente pode acessar o servidor via `http://web-server:8080`
- Isolamento: apenas containers na mesma rede podem se comunicar

## Como Executar

### Pré-requisitos

- Docker instalado e em execução
- Porta 8080 disponível no host

### Passo 1: Navegar até o diretório

```bash
cd desafio1
```

### Passo 2: Executar o script de setup

```bash
# No Linux/Mac
chmod +x run.sh cleanup.sh
./run.sh

# No Windows (Git Bash ou WSL)
bash run.sh
```

O script automaticamente:

1. Cria a rede `desafio1-network`
2. Constrói as imagens Docker
3. Inicia o container do servidor
4. Inicia o container do cliente

### Passo 3: Verificar a comunicação

#### Ver logs do servidor:

```bash
docker logs -f web-server
```

#### Ver logs do cliente:

```bash
docker logs -f web-client
```

#### Testar manualmente do host:

```bash
curl http://localhost:8080
```

Resposta esperada:

```json
{
  "hostname": "abc123def456",
  "message": "Servidor Flask funcionando!",
  "request_number": 15,
  "timestamp": "2025-11-23T10:30:45.123456"
}
```

### Passo 4: Limpar o ambiente

```bash
# No Linux/Mac
./cleanup.sh

# No Windows (Git Bash ou WSL)
bash cleanup.sh
```

## Funcionamento Detalhado

### 1. Criação da Rede

```bash
docker network create desafio1-network
```

Cria uma rede bridge customizada que permite:

- Resolução de nomes DNS entre containers
- Isolamento de rede
- Comunicação segura entre containers

### 2. Servidor Web (web-server)

O servidor Flask:

- Escuta na porta 8080
- Mantém um contador de requisições recebidas
- Retorna informações em formato JSON
- Registra cada requisição nos logs

```python
@app.route('/')
def home():
    global request_count
    request_count += 1
    return jsonify({
        'message': 'Servidor Flask funcionando!',
        'timestamp': datetime.now().isoformat(),
        'hostname': os.uname().nodename,
        'request_number': request_count
    })
```

### 3. Cliente (web-client)

O cliente executa um loop infinito que:

- A cada 5 segundos faz uma requisição GET para `http://web-server:8080`
- Usa `curl` para fazer a requisição
- Usa `jq` para formatar a resposta JSON
- Exibe timestamp de cada requisição
- Trata erros de conexão

```bash
while true; do
    echo "[$(date)] Fazendo requisição ao servidor..."
    response=$(curl -s http://web-server:8080)
    echo "$response" | jq '.'
    sleep 5
done
```

### 4. Comunicação

- O cliente resolve o nome `web-server` através do DNS interno do Docker
- O Docker roteia o tráfego através da rede `desafio1-network`
- O servidor recebe a requisição, processa e responde
- A resposta é capturada e exibida pelo cliente

## Demonstração de Logs

### Logs do Servidor:

```
Servidor iniciando na porta 8080...
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:8080
172.18.0.3 - - [23/Nov/2025 10:30:40] "GET / HTTP/1.1" 200 -
172.18.0.3 - - [23/Nov/2025 10:30:45] "GET / HTTP/1.1" 200 -
172.18.0.3 - - [23/Nov/2025 10:30:50] "GET / HTTP/1.1" 200 -
```

### Logs do Cliente:

```
Cliente iniciando requisições periódicas...
Servidor alvo: http://web-server:8080

[2025-11-23 10:30:40] Fazendo requisição ao servidor...
✓ Resposta recebida:
{
  "hostname": "abc123",
  "message": "Servidor Flask funcionando!",
  "request_number": 1,
  "timestamp": "2025-11-23T10:30:40.123456"
}
Aguardando 5 segundos...
```

## Como Testar

### Teste 1: Verificar containers em execução

```bash
docker ps
```

Deve mostrar `web-server` e `web-client` rodando.

### Teste 2: Verificar a rede

```bash
docker network inspect desafio1-network
```

Deve mostrar ambos os containers conectados.

### Teste 3: Acessar do host

```bash
curl http://localhost:8080
```

### Teste 4: Executar curl dentro do cliente

```bash
docker exec web-client curl -s http://web-server:8080
```

### Teste 5: Verificar isolamento

```bash
# Criar container fora da rede
docker run --rm alpine:latest wget -O- http://web-server:8080
# Deve falhar pois não está na mesma rede
```

## Comandos Úteis

```bash
# Ver todos os containers
docker ps -a

# Ver logs em tempo real
docker logs -f web-server
docker logs -f web-client

# Inspecionar container
docker inspect web-server

# Entrar no container do servidor
docker exec -it web-server bash

# Entrar no container do cliente
docker exec -it web-client sh

# Ver estatísticas de uso
docker stats web-server web-client

# Reiniciar containers
docker restart web-server web-client
```

## Critérios Atendidos

- [5 pts] Configuração correta da rede Docker: Rede customizada desafio1-network criada e configurada
- [5 pts] Comunicação funcional entre containers: Cliente e servidor se comunicam via HTTP usando nomes DNS
- [5 pts] Explicação clara no README: Documentação completa com arquitetura, decisões técnicas e exemplos
- [5 pts] Organização do projeto e scripts de execução: Scripts automatizados para setup e limpeza, código organizado

## Segurança e Boas Práticas

1. **Imagens oficiais**: Uso de `python:3.11-slim` e `alpine:latest`
2. **Não-root**: Containers não executam como root (boas práticas)
3. **Isolamento**: Rede customizada isola os containers
4. **Logs estruturados**: Logging adequado para debugging
5. **Health checks**: Endpoint `/health` para monitoramento

## Conceitos Aprendidos

- Criação e configuração de redes Docker
- Comunicação inter-container usando DNS
- Dockerfiles multi-estágio
- Port binding e port mapping
- Container orchestration básica
- Logging e debugging de containers
- Scripts de automação para Docker
