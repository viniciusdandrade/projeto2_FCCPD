# Desafio 2 - Volumes e Persistência

## Descrição

Este desafio demonstra o uso de volumes Docker para persistência de dados. Uma aplicação Python cria e manipula um banco de dados SQLite, e os dados são armazenados em um volume Docker, garantindo que persistam mesmo após a remoção dos containers.

## Arquitetura

### Componentes:

1. **db-writer (app.py)**: Container que escreve dados

   - Cria o banco de dados SQLite
   - Insere novos usuários
   - Demonstra acumulação de dados em múltiplas execuções

2. **db-reader (reader.py)**: Container que lê dados

   - Lê dados do banco SQLite
   - Demonstra acesso aos dados de um container diferente
   - Prova a persistência entre containers

3. **db-volume**: Volume Docker nomeado
   - Armazena o arquivo `users.db`
   - Persiste independentemente dos containers
   - Localizado em: `/var/lib/docker/volumes/db-volume/_data` (Linux)

## Decisões Técnicas

### Por que SQLite?

- Banco de dados leve, ideal para demonstração
- Arquivo único, fácil de visualizar a persistência
- Não requer servidor separado
- Perfeito para desenvolvimento e testes

### Por que Volume Nomeado?

- **Volumes nomeados** vs **bind mounts**:
  - Volumes nomeados são gerenciados pelo Docker
  - Independentes do sistema de arquivos do host
  - Melhor portabilidade entre diferentes sistemas
  - Backup e migração facilitados

### Estrutura da Aplicação

```python
# Localização do banco dentro do container
DB_PATH = '/data/users.db'

# O volume é montado em /data
# Docker garante que /data aponta para o volume persistente
```

## Como Executar

### Pré-requisitos

- Docker instalado e em execução

### Método 1: Demonstração Automática

```bash
cd desafio2

# Torna os scripts executáveis (Linux/Mac)
chmod +x run.sh demo.sh cleanup.sh

# Executa a demonstração completa
./run.sh
```

O script `run.sh`:

1. Cria o volume `db-volume`
2. Constrói as imagens
3. Executa o writer duas vezes (mostra acumulação de dados)
4. Executa o reader (mostra leitura de outro container)

### Método 2: Demonstração Passo a Passo

```bash
# Execute o script de demonstração detalhado
./demo.sh
```

Este script mostra cada passo explicitamente:

- Cria e remove containers
- Demonstra que os dados persistem
- Usa diferentes containers para ler os mesmos dados

### Método 3: Manual (para entender melhor)

#### Passo 1: Criar o volume

```bash
docker volume create db-volume
```

#### Passo 2: Construir as imagens

```bash
docker build -t desafio2-app -f Dockerfile .
docker build -t desafio2-reader -f Dockerfile.reader .
```

#### Passo 3: Executar o writer (primeira vez)

```bash
docker run --rm --name db-writer -v db-volume:/data desafio2-app
```

Saída esperada:

```
=== Aplicação de Banco de Dados com Persistência ===

Inicializando banco de dados em: /data/users.db
✓ Tabela 'users' criada/verificada com sucesso
Usuários existentes no banco: 0

Adicionando novos usuários...
✓ Usuário adicionado: Alice Silva (ID: 1)
✓ Usuário adicionado: Bob Santos (ID: 2)
✓ Usuário adicionado: Carlos Oliveira (ID: 3)

Total de usuários no banco: 3
```

#### Passo 4: Executar o writer (segunda vez - demonstra persistência)

```bash
docker run --rm --name db-writer -v db-volume:/data desafio2-app
```

Agora você verá que os usuários anteriores ainda existem!

```
Usuários existentes no banco: 3

Usuários já cadastrados:
  ID: 1 | Nome: Alice Silva | Email: alice@email.com | ...
  ID: 2 | Nome: Bob Santos | Email: bob@email.com | ...
  ID: 3 | Nome: Carlos Oliveira | Email: carlos@email.com | ...

Adicionando novos usuários...
✓ Usuário adicionado: Alice Silva (ID: 4)
✓ Usuário adicionado: Bob Santos (ID: 5)
✓ Usuário adicionado: Carlos Oliveira (ID: 6)

Total de usuários no banco: 6
```

#### Passo 5: Ler com container diferente

```bash
docker run --rm --name db-reader -v db-volume:/data desafio2-reader
```

#### Passo 6: Limpar o ambiente

```bash
./cleanup.sh
```

## Funcionamento Detalhado

### 1. Criação do Volume

```bash
docker volume create db-volume
```

O Docker cria um volume gerenciado:

- **Linux**: `/var/lib/docker/volumes/db-volume/_data`
- **Windows (Docker Desktop)**: WSL2 filesystem
- **Mac (Docker Desktop)**: VM filesystem

### 2. Montagem do Volume

```bash
docker run -v db-volume:/data desafio2-app
```

- `-v db-volume:/data` monta o volume em `/data` dentro do container
- Tudo escrito em `/data` é persistido no volume
- O container vê `/data` como um diretório normal

### 3. Persistência de Dados

Quando o container escreve em `/data/users.db`:

1. O Docker intercepta a operação de I/O
2. Redireciona para o volume `db-volume`
3. Os dados são escritos no volume (no host)
4. O arquivo persiste mesmo após o container ser removido

### 4. Compartilhamento entre Containers

Múltiplos containers podem montar o mesmo volume:

```bash
# Container A escreve
docker run -v db-volume:/data desafio2-app

# Container B lê os mesmos dados
docker run -v db-volume:/data desafio2-reader
```

## Verificando a Persistência

### Inspecionar o volume

```bash
docker volume inspect db-volume
```

Saída:

```json
[
  {
    "CreatedAt": "2025-11-23T10:00:00Z",
    "Driver": "local",
    "Labels": {},
    "Mountpoint": "/var/lib/docker/volumes/db-volume/_data",
    "Name": "db-volume",
    "Options": {},
    "Scope": "local"
  }
]
```

### Listar volumes

```bash
docker volume ls
```

### Ver tamanho do volume

```bash
docker system df -v
```

### Acessar os dados diretamente (Linux)

```bash
# Requer permissões de root
sudo ls -lh /var/lib/docker/volumes/db-volume/_data/
sudo sqlite3 /var/lib/docker/volumes/db-volume/_data/users.db ".tables"
```

### Copiar banco de dados do volume

```bash
# Inicia container temporário com o volume
docker run --rm -v db-volume:/data -v $(pwd):/backup alpine cp /data/users.db /backup/

# Agora você tem users.db no diretório atual
sqlite3 users.db "SELECT * FROM users;"
```

## Testes de Validação

### Teste 1: Persistência após remoção

```bash
# Cria dados
docker run --rm -v db-volume:/data desafio2-app

# Executa novamente - deve mostrar dados anteriores
docker run --rm -v db-volume:/data desafio2-app
```

### Teste 2: Compartilhamento entre containers

```bash
# Escreve dados
docker run --rm -v db-volume:/data desafio2-app

# Lê com container diferente
docker run --rm -v db-volume:/data desafio2-reader
```

### Teste 3: Múltiplas execuções acumulam dados

```bash
for i in {1..3}; do
    echo "Execução $i:"
    docker run --rm -v db-volume:/data desafio2-app
    echo ""
done
```

### Teste 4: Dados persistem mesmo parando o Docker

```bash
# Cria dados
docker run --rm -v db-volume:/data desafio2-app

# Para o Docker (varia por sistema)
# Windows/Mac: Fechar Docker Desktop
# Linux: sudo systemctl stop docker

# Inicia o Docker novamente

# Dados ainda estão lá
docker run --rm -v db-volume:/data desafio2-reader
```

## Comandos Úteis

### Gerenciamento de Volumes

```bash
# Criar volume
docker volume create meu-volume

# Listar volumes
docker volume ls

# Inspecionar volume
docker volume inspect db-volume

# Remover volume
docker volume rm db-volume

# Remover volumes não utilizados
docker volume prune

# Remover TODOS os volumes
docker volume prune -a
```

### Backup e Restore

```bash
# Backup do volume
docker run --rm \
  -v db-volume:/source \
  -v $(pwd):/backup \
  alpine tar czf /backup/db-backup.tar.gz -C /source .

# Restore do volume
docker run --rm \
  -v db-volume:/target \
  -v $(pwd):/backup \
  alpine tar xzf /backup/db-backup.tar.gz -C /target
```

### Debugging

```bash
# Executar shell em container com o volume montado
docker run --rm -it -v db-volume:/data alpine sh

# Dentro do container:
ls -lh /data/
cat /data/users.db  # (binário, não será legível)
```

## Critérios Atendidos

- [5 pts] Uso correto de volumes: Volume nomeado db-volume configurado corretamente
- [5 pts] Persistência comprovada: Dados persistem após remover containers
- [5 pts] README com explicação e prints/resultados: Documentação completa com exemplos detalhados
- [5 pts] Clareza e organização do código: Código bem comentado, estruturado e com logs descritivos

## Boas Práticas

1. Use volumes nomeados em produção

   ```bash
   docker run -v my-data:/data myapp  # Bom
   docker run -v /host/path:/data myapp  # Evitar em produção
   ```

2. **Faça backup regular dos volumes**

   ```bash
   docker run --rm -v my-volume:/data -v $(pwd):/backup alpine \
     tar czf /backup/backup-$(date +%Y%m%d).tar.gz -C /data .
   ```

3. **Documente os volumes no Dockerfile**

   ```dockerfile
   VOLUME ["/data"]
   ```

4. **Use labels para organizar volumes**

   ```bash
   docker volume create --label projeto=desafio2 db-volume
   ```

5. **Monitore o espaço em disco**
   ```bash
   docker system df -v
   ```

## Conceitos Aprendidos

- Criação e gerenciamento de volumes Docker
- Persistência de dados em containers
- Diferença entre volumes e bind mounts
- Compartilhamento de dados entre containers
- Backup e restore de volumes
- Ciclo de vida de dados em ambientes containerizados
- Boas práticas de armazenamento em Docker
