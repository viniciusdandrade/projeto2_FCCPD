from flask import Flask, jsonify, request as flask_request
import requests
from datetime import datetime, timedelta
import os

app = Flask(__name__)

USER_SERVICE_URL = os.getenv('USER_SERVICE_URL', 'http://localhost:5001')

@app.route('/')
def home():
    return jsonify({
        'service': 'User Info Service B',
        'version': '1.0.0',
        'description': 'Microsserviço que consome o Service A e fornece informações enriquecidas',
        'timestamp': datetime.now().isoformat(),
        'dependencies': {
            'user-service': USER_SERVICE_URL
        },
        'endpoints': {
            '/': 'Informações do serviço',
            '/health': 'Health check',
            '/user-info': 'Informações enriquecidas de todos os usuários',
            '/user-info/<id>': 'Informações enriquecidas de um usuário',
            '/user-summary': 'Resumo estatístico dos usuários'
        }
    })

@app.route('/health')
def health():
    user_service_status = 'unknown'
    try:
        response = requests.get(f'{USER_SERVICE_URL}/health', timeout=5)
        if response.status_code == 200:
            user_service_status = 'connected'
        else:
            user_service_status = 'error'
    except requests.exceptions.RequestException:
        user_service_status = 'unreachable'
    
    return jsonify({
        'status': 'healthy',
        'service': 'user-info-service',
        'timestamp': datetime.now().isoformat(),
        'dependencies': {
            'user-service': user_service_status
        }
    })

def enrich_user_data(user):
    joined_date = datetime.strptime(user['joined_date'], '%Y-%m-%d')
    days_active = (datetime.now() - joined_date).days
    years = days_active // 365
    months = (days_active % 365) // 30
    
    enriched = user.copy()
    enriched['enriched_info'] = {
        'days_since_joined': days_active,
        'years_active': years,
        'months_active': months,
        'status_text': 'Ativo' if user['active'] else 'Inativo',
        'profile_summary': f"{user['name']} - {user['role']} {'(Ativo)' if user['active'] else '(Inativo)'}",
        'member_since': f"{user['name']} é membro desde {user['joined_date']} ({years} anos, {months} meses)"
    }
    
    return enriched

@app.route('/user-info')
def get_all_user_info():
    try:
        response = requests.get(f'{USER_SERVICE_URL}/users', timeout=10)
        
        if response.status_code != 200:
            return jsonify({
                'error': 'Failed to fetch users from user-service',
                'status_code': response.status_code
            }), 502
        
        data = response.json()
        users = data.get('users', [])
        
        enriched_users = [enrich_user_data(user) for user in users]
        
        return jsonify({
            'service': 'user-info-service',
            'source': 'user-service',
            'count': len(enriched_users),
            'users': enriched_users,
            'processed_at': datetime.now().isoformat()
        })
        
    except requests.exceptions.RequestException as e:
        return jsonify({
            'error': 'Failed to communicate with user-service',
            'details': str(e)
        }), 503

@app.route('/user-info/<int:user_id>')
def get_user_info(user_id):
    try:
        response = requests.get(f'{USER_SERVICE_URL}/users/{user_id}', timeout=10)
        
        if response.status_code == 404:
            return jsonify({
                'error': 'User not found',
                'user_id': user_id
            }), 404
        
        if response.status_code != 200:
            return jsonify({
                'error': 'Failed to fetch user from user-service',
                'status_code': response.status_code
            }), 502
        
        data = response.json()
        user = data.get('user')
        
        enriched_user = enrich_user_data(user)
        
        return jsonify({
            'service': 'user-info-service',
            'source': 'user-service',
            'user': enriched_user,
            'processed_at': datetime.now().isoformat()
        })
        
    except requests.exceptions.RequestException as e:
        return jsonify({
            'error': 'Failed to communicate with user-service',
            'details': str(e)
        }), 503

@app.route('/user-summary')
def get_user_summary():
    try:
        response = requests.get(f'{USER_SERVICE_URL}/users', timeout=10)
        
        if response.status_code != 200:
            return jsonify({
                'error': 'Failed to fetch users from user-service',
                'status_code': response.status_code
            }), 502
        
        data = response.json()
        users = data.get('users', [])
        
        total_users = len(users)
        active_users = sum(1 for u in users if u['active'])
        inactive_users = total_users - active_users
        
        roles = {}
        for user in users:
            role = user['role']
            roles[role] = roles.get(role, 0) + 1
        
        total_days = 0
        for user in users:
            joined_date = datetime.strptime(user['joined_date'], '%Y-%m-%d')
            days = (datetime.now() - joined_date).days
            total_days += days
        
        avg_days = total_days / total_users if total_users > 0 else 0
        
        return jsonify({
            'service': 'user-info-service',
            'source': 'user-service',
            'summary': {
                'total_users': total_users,
                'active_users': active_users,
                'inactive_users': inactive_users,
                'active_percentage': round((active_users / total_users * 100), 2) if total_users > 0 else 0,
                'roles_distribution': roles,
                'average_days_as_member': round(avg_days, 0),
                'average_years_as_member': round(avg_days / 365, 1)
            },
            'processed_at': datetime.now().isoformat()
        })
        
    except requests.exceptions.RequestException as e:
        return jsonify({
            'error': 'Failed to communicate with user-service',
            'details': str(e)
        }), 503

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5002))
    print(f"Microsserviço B (User Info) iniciando na porta {port}...")
    print(f"Conectando ao User Service em: {USER_SERVICE_URL}")
    app.run(host='0.0.0.0', port=port, debug=True)
