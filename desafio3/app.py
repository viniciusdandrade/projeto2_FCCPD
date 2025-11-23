from flask import Flask, jsonify, request
import psycopg2
import redis
import os
import json
from datetime import datetime

app = Flask(__name__)

DB_CONFIG = {
    'host': 'db',
    'database': 'appdb',
    'user': 'user',
    'password': 'password'
}

REDIS_HOST = os.getenv('REDIS_HOST', 'cache')
REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))

try:
    cache = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
    cache.ping()
    print(f"Conectado ao Redis em {REDIS_HOST}:{REDIS_PORT}")
except Exception as e:
    print(f"Erro ao conectar ao Redis: {e}")
    cache = None

def get_db_connection():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        print(f"Erro ao conectar ao banco: {e}")
        return None

@app.route('/')
def home():
    return jsonify({
        'service': 'Web Application',
        'status': 'running',
        'timestamp': datetime.now().isoformat(),
        'endpoints': {
            '/': 'Informações do sistema',
            '/health': 'Health check',
            '/users': 'Lista todos os usuários (GET) ou cria novo (POST)',
            '/users/<id>': 'Detalhes de um usuário',
            '/cache/set': 'Define valor no cache (POST)',
            '/cache/get/<key>': 'Obtém valor do cache',
            '/stats': 'Estatísticas do sistema'
        }
    })

@app.route('/health')
def health():
    db_status = 'connected'
    cache_status = 'connected'
    
    try:
        conn = get_db_connection()
        if conn:
            conn.close()
    except:
        db_status = 'disconnected'
    
    try:
        if cache:
            cache.ping()
    except:
        cache_status = 'disconnected'
    
    return jsonify({
        'status': 'healthy',
        'database': db_status,
        'cache': cache_status,
        'timestamp': datetime.now().isoformat()
    })

@app.route('/users', methods=['GET', 'POST'])
def users():
    if request.method == 'GET':
        cached_users = None
        if cache:
            try:
                cached_users = cache.get('users:all')
                if cached_users:
                    print("Usuários obtidos do cache")
                    return jsonify({
                        'source': 'cache',
                        'users': json.loads(cached_users)
                    })
            except Exception as e:
                print(f"Erro ao acessar cache: {e}")
        
        conn = get_db_connection()
        if not conn:
            return jsonify({'error': 'Database connection failed'}), 500
        
        try:
            cur = conn.cursor()
            cur.execute('SELECT id, name, email, created_at FROM users ORDER BY id')
            rows = cur.fetchall()
            
            users_list = [
                {
                    'id': row[0],
                    'name': row[1],
                    'email': row[2],
                    'created_at': row[3].isoformat() if row[3] else None
                }
                for row in rows
            ]
            
            if cache:
                try:
                    cache.setex('users:all', 60, json.dumps(users_list))
                    print("Usuários armazenados no cache")
                except Exception as e:
                    print(f"Erro ao armazenar no cache: {e}")
            
            cur.close()
            conn.close()
            
            return jsonify({
                'source': 'database',
                'users': users_list
            })
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    elif request.method == 'POST':
        data = request.get_json()
        
        if not data or 'name' not in data or 'email' not in data:
            return jsonify({'error': 'Name and email are required'}), 400
        
        conn = get_db_connection()
        if not conn:
            return jsonify({'error': 'Database connection failed'}), 500
        
        try:
            cur = conn.cursor()
            cur.execute(
                'INSERT INTO users (name, email) VALUES (%s, %s) RETURNING id',
                (data['name'], data['email'])
            )
            user_id = cur.fetchone()[0]
            conn.commit()
            cur.close()
            conn.close()
            
            if cache:
                try:
                    cache.delete('users:all')
                    print("Cache invalidado")
                except Exception as e:
                    print(f"Erro ao invalidar cache: {e}")
            
            return jsonify({
                'message': 'User created successfully',
                'id': user_id
            }), 201
        except Exception as e:
            return jsonify({'error': str(e)}), 500

@app.route('/users/<int:user_id>')
def get_user(user_id):
    cache_key = f'user:{user_id}'
    if cache:
        try:
            cached_user = cache.get(cache_key)
            if cached_user:
                print(f"Usuário {user_id} obtido do cache")
                return jsonify({
                    'source': 'cache',
                    'user': json.loads(cached_user)
                })
        except Exception as e:
            print(f"Erro ao acessar cache: {e}")
    
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500
    
    try:
        cur = conn.cursor()
        cur.execute('SELECT id, name, email, created_at FROM users WHERE id = %s', (user_id,))
        row = cur.fetchone()
        
        if not row:
            return jsonify({'error': 'User not found'}), 404
        
        user_data = {
            'id': row[0],
            'name': row[1],
            'email': row[2],
            'created_at': row[3].isoformat() if row[3] else None
        }
        
        if cache:
            try:
                cache.setex(cache_key, 300, json.dumps(user_data))
                print(f"Usuário {user_id} armazenado no cache")
            except Exception as e:
                print(f"Erro ao armazenar no cache: {e}")
        
        cur.close()
        conn.close()
        
        return jsonify({
            'source': 'database',
            'user': user_data
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/cache/set', methods=['POST'])
def cache_set():
    if not cache:
        return jsonify({'error': 'Cache not available'}), 503
    
    data = request.get_json()
    if not data or 'key' not in data or 'value' not in data:
        return jsonify({'error': 'Key and value are required'}), 400
    
    try:
        ttl = data.get('ttl', 300)
        cache.setex(data['key'], ttl, data['value'])
        return jsonify({
            'message': 'Value stored in cache',
            'key': data['key'],
            'ttl': ttl
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/cache/get/<key>')
def cache_get(key):
    if not cache:
        return jsonify({'error': 'Cache not available'}), 503
    
    try:
        value = cache.get(key)
        if value is None:
            return jsonify({'error': 'Key not found'}), 404
        
        ttl = cache.ttl(key)
        return jsonify({
            'key': key,
            'value': value,
            'ttl': ttl
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/stats')
def stats():
    db_count = 0
    cache_keys = 0
    
    conn = get_db_connection()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute('SELECT COUNT(*) FROM users')
            db_count = cur.fetchone()[0]
            cur.close()
            conn.close()
        except:
            pass
    
    if cache:
        try:
            cache_keys = cache.dbsize()
        except:
            pass
    
    return jsonify({
        'database': {
            'users_count': db_count
        },
        'cache': {
            'keys_count': cache_keys
        },
        'timestamp': datetime.now().isoformat()
    })

if __name__ == '__main__':
    print("Iniciando aplicação web...")
    print(f"Banco de dados: {DB_CONFIG['host']}")
    print(f"Cache: {REDIS_HOST}:{REDIS_PORT}")
    app.run(host='0.0.0.0', port=5000, debug=True)
