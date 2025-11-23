import sqlite3
from datetime import datetime
import time
import os

DB_PATH = '/data/users.db'

def init_database():
    print(f"Inicializando banco de dados em: {DB_PATH}")
    
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    print("Tabela 'users' criada/verificada com sucesso")
    
    return conn

def insert_user(conn, name, email):
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO users (name, email, created_at) VALUES (?, ?, ?)',
        (name, email, datetime.now().isoformat())
    )
    conn.commit()
    return cursor.lastrowid

def list_users(conn):
    cursor = conn.cursor()
    cursor.execute('SELECT id, name, email, created_at FROM users ORDER BY id')
    return cursor.fetchall()

def count_users(conn):
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM users')
    return cursor.fetchone()[0]

def main():
    print("=== Aplicação de Banco de Dados com Persistência ===")
    print()
    
    conn = init_database()
    
    existing_users = count_users(conn)
    print(f"Usuários existentes no banco: {existing_users}")
    print()
    
    if existing_users > 0:
        print("Usuários já cadastrados:")
        users = list_users(conn)
        for user in users:
            print(f"  ID: {user[0]} | Nome: {user[1]} | Email: {user[2]} | Criado em: {user[3]}")
        print()
    
    print("Adicionando novos usuários...")
    new_users = [
        ('Alice Silva', 'alice@email.com'),
        ('Bob Santos', 'bob@email.com'),
        ('Carlos Oliveira', 'carlos@email.com'),
    ]
    
    for name, email in new_users:
        user_id = insert_user(conn, name, email)
        print(f"Usuário adicionado: {name} (ID: {user_id})")
    
    print()
    
    total = count_users(conn)
    print(f"Total de usuários no banco: {total}")
    print()
    print("Todos os usuários cadastrados:")
    users = list_users(conn)
    for user in users:
        print(f"  ID: {user[0]} | Nome: {user[1]} | Email: {user[2]} | Criado em: {user[3]}")
    
    conn.close()
    print()
    print("Dados persistidos com sucesso em /data/users.db")
    print("Mesmo após remover o container, os dados permanecerão no volume!")

if __name__ == '__main__':
    main()
