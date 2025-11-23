-- Script de inicialização do banco de dados

-- Cria a tabela de usuários
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Cria índice no email para buscas rápidas
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);

-- Insere alguns usuários de exemplo
INSERT INTO users (name, email) VALUES
    ('João Silva', 'joao@email.com'),
    ('Maria Santos', 'maria@email.com'),
    ('Pedro Oliveira', 'pedro@email.com'),
    ('Ana Costa', 'ana@email.com')
ON CONFLICT (email) DO NOTHING;

-- Confirma a criação
SELECT 'Database initialized successfully!' as message;
