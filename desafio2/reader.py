import sqlite3
import sys

DB_PATH = '/data/users.db'

def read_database():
    print("=== Leitor de Banco de Dados ===")
    print(f"Lendo banco de dados de: {DB_PATH}")
    print()
    
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='users'"
        )
        if not cursor.fetchone():
            print("Tabela 'users' não encontrada!")
            return
        
        cursor.execute('SELECT id, name, email, created_at FROM users ORDER BY id')
        users = cursor.fetchall()
        
        if not users:
            print("Nenhum usuário encontrado no banco de dados.")
        else:
            print(f"Total de usuários encontrados: {len(users)}")
            print()
            print("Usuários cadastrados:")
            print("-" * 80)
            for user in users:
                print(f"ID: {user[0]:<4} | Nome: {user[1]:<20} | Email: {user[2]:<25} | Criado em: {user[3]}")
            print("-" * 80)
        
        conn.close()
        print()
        print("Dados lidos com sucesso do volume persistente!")
        
    except sqlite3.OperationalError as e:
        print(f"Erro ao acessar o banco de dados: {e}")
        sys.exit(1)

if __name__ == '__main__':
    read_database()
