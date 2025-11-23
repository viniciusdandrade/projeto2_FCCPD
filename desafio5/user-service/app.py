from flask import Flask, jsonify
from datetime import datetime

app = Flask(__name__)

USERS_DB = [
    {'id': 1, 'name': 'Alice Silva', 'email': 'alice@email.com', 'department': 'Engineering'},
    {'id': 2, 'name': 'Bob Santos', 'email': 'bob@email.com', 'department': 'Design'},
    {'id': 3, 'name': 'Carlos Oliveira', 'email': 'carlos@email.com', 'department': 'Management'},
    {'id': 4, 'name': 'Diana Costa', 'email': 'diana@email.com', 'department': 'Engineering'},
    {'id': 5, 'name': 'Eduardo Lima', 'email': 'eduardo@email.com', 'department': 'Sales'}
]

@app.route('/')
def home():
    return jsonify({
        'service': 'User Service',
        'version': '1.0.0',
        'description': 'Gerenciamento de usuários',
        'endpoints': {
            '/users': 'Lista todos os usuários',
            '/users/<id>': 'Detalhes de um usuário'
        }
    })

@app.route('/health')
def health():
    return jsonify({'status': 'healthy', 'service': 'user-service'})

@app.route('/users')
def get_users():
    return jsonify({
        'service': 'user-service',
        'timestamp': datetime.now().isoformat(),
        'count': len(USERS_DB),
        'users': USERS_DB
    })

@app.route('/users/<int:user_id>')
def get_user(user_id):
    user = next((u for u in USERS_DB if u['id'] == user_id), None)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    return jsonify({
        'service': 'user-service',
        'user': user
    })

if __name__ == '__main__':
    print("User Service iniciando na porta 5001...")
    app.run(host='0.0.0.0', port=5001, debug=True)
