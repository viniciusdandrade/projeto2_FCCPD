from flask import Flask, jsonify
from datetime import datetime
import os

app = Flask(__name__)

USERS_DB = [
    {
        'id': 1,
        'name': 'Alice Silva',
        'email': 'alice@email.com',
        'role': 'Developer',
        'active': True,
        'joined_date': '2023-01-15'
    },
    {
        'id': 2,
        'name': 'Bob Santos',
        'email': 'bob@email.com',
        'role': 'Designer',
        'active': True,
        'joined_date': '2023-03-20'
    },
    {
        'id': 3,
        'name': 'Carlos Oliveira',
        'email': 'carlos@email.com',
        'role': 'Manager',
        'active': False,
        'joined_date': '2022-11-10'
    },
    {
        'id': 4,
        'name': 'Diana Costa',
        'email': 'diana@email.com',
        'role': 'Developer',
        'active': True,
        'joined_date': '2023-05-01'
    },
    {
        'id': 5,
        'name': 'Eduardo Lima',
        'email': 'eduardo@email.com',
        'role': 'Analyst',
        'active': True,
        'joined_date': '2023-07-12'
    }
]

@app.route('/')
def home():
    return jsonify({
        'service': 'User Service A',
        'version': '1.0.0',
        'description': 'Microsserviço responsável por gerenciar usuários',
        'timestamp': datetime.now().isoformat(),
        'endpoints': {
            '/': 'Informações do serviço',
            '/health': 'Health check',
            '/users': 'Lista todos os usuários',
            '/users/<id>': 'Detalhes de um usuário específico',
            '/users/active': 'Lista apenas usuários ativos',
            '/users/inactive': 'Lista apenas usuários inativos'
        }
    })

@app.route('/health')
def health():
    return jsonify({
        'status': 'healthy',
        'service': 'user-service',
        'timestamp': datetime.now().isoformat(),
        'uptime': 'running'
    })

@app.route('/users')
def get_users():
    return jsonify({
        'service': 'user-service',
        'count': len(USERS_DB),
        'users': USERS_DB
    })

@app.route('/users/<int:user_id>')
def get_user(user_id):
    user = next((u for u in USERS_DB if u['id'] == user_id), None)
    
    if not user:
        return jsonify({
            'error': 'User not found',
            'user_id': user_id
        }), 404
    
    return jsonify({
        'service': 'user-service',
        'user': user
    })

@app.route('/users/active')
def get_active_users():
    active_users = [u for u in USERS_DB if u['active']]
    return jsonify({
        'service': 'user-service',
        'count': len(active_users),
        'users': active_users
    })

@app.route('/users/inactive')
def get_inactive_users():
    inactive_users = [u for u in USERS_DB if not u['active']]
    return jsonify({
        'service': 'user-service',
        'count': len(inactive_users),
        'users': inactive_users
    })

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5001))
    print(f"Microsserviço A (Users) iniciando na porta {port}...")
    app.run(host='0.0.0.0', port=port, debug=True)
