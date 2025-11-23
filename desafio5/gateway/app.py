from flask import Flask, jsonify, request
import requests
from datetime import datetime
import os

app = Flask(__name__)

USER_SERVICE_URL = os.getenv('USER_SERVICE_URL', 'http://user-service:5001')
ORDER_SERVICE_URL = os.getenv('ORDER_SERVICE_URL', 'http://order-service:5002')

stats = {
    'total_requests': 0,
    'users_requests': 0,
    'orders_requests': 0,
    'errors': 0
}

@app.route('/')
def home():
    return jsonify({
        'service': 'API Gateway',
        'version': '1.0.0',
        'description': 'Ponto único de entrada para todos os microsserviços',
        'timestamp': datetime.now().isoformat(),
        'services': {
            'user-service': USER_SERVICE_URL,
            'order-service': ORDER_SERVICE_URL
        },
        'endpoints': {
            '/': 'Informações do gateway',
            '/health': 'Health check de todos os serviços',
            '/stats': 'Estatísticas do gateway',
            '/users': 'Lista usuários (proxy para user-service)',
            '/users/<id>': 'Detalhes de usuário (proxy)',
            '/orders': 'Lista pedidos (proxy para order-service)',
            '/orders/<id>': 'Detalhes de pedido (proxy)',
            '/users/<id>/complete': 'Dados completos (usuário + pedidos - agregação)'
        }
    })

@app.route('/health')
def health():
    stats['total_requests'] += 1
    
    services_health = {}
    overall_status = 'healthy'
    
    try:
        response = requests.get(f'{USER_SERVICE_URL}/health', timeout=5)
        services_health['user-service'] = 'healthy' if response.status_code == 200 else 'unhealthy'
    except:
        services_health['user-service'] = 'unreachable'
        overall_status = 'degraded'
    
    try:
        response = requests.get(f'{ORDER_SERVICE_URL}/health', timeout=5)
        services_health['order-service'] = 'healthy' if response.status_code == 200 else 'unhealthy'
    except:
        services_health['order-service'] = 'unreachable'
        overall_status = 'degraded'
    
    return jsonify({
        'gateway': 'healthy',
        'overall_status': overall_status,
        'services': services_health,
        'timestamp': datetime.now().isoformat()
    })

@app.route('/stats')
def get_stats():
    return jsonify({
        'gateway': 'api-gateway',
        'statistics': stats,
        'timestamp': datetime.now().isoformat()
    })

@app.route('/users')
def get_users():
    stats['total_requests'] += 1
    stats['users_requests'] += 1
    
    try:
        response = requests.get(f'{USER_SERVICE_URL}/users', timeout=10)
        
        if response.status_code != 200:
            stats['errors'] += 1
            return jsonify({'error': 'User service error'}), response.status_code
        
        data = response.json()
        data['via'] = 'api-gateway'
        return jsonify(data)
        
    except requests.exceptions.RequestException as e:
        stats['errors'] += 1
        return jsonify({
            'error': 'Failed to reach user service',
            'details': str(e)
        }), 503

@app.route('/users/<int:user_id>')
def get_user(user_id):
    stats['total_requests'] += 1
    stats['users_requests'] += 1
    
    try:
        response = requests.get(f'{USER_SERVICE_URL}/users/{user_id}', timeout=10)
        
        if response.status_code == 404:
            return jsonify({'error': 'User not found'}), 404
        
        if response.status_code != 200:
            stats['errors'] += 1
            return jsonify({'error': 'User service error'}), response.status_code
        
        data = response.json()
        data['via'] = 'api-gateway'
        return jsonify(data)
        
    except requests.exceptions.RequestException as e:
        stats['errors'] += 1
        return jsonify({
            'error': 'Failed to reach user service',
            'details': str(e)
        }), 503

@app.route('/orders')
def get_orders():
    stats['total_requests'] += 1
    stats['orders_requests'] += 1
    
    try:
        response = requests.get(f'{ORDER_SERVICE_URL}/orders', timeout=10)
        
        if response.status_code != 200:
            stats['errors'] += 1
            return jsonify({'error': 'Order service error'}), response.status_code
        
        data = response.json()
        data['via'] = 'api-gateway'
        return jsonify(data)
        
    except requests.exceptions.RequestException as e:
        stats['errors'] += 1
        return jsonify({
            'error': 'Failed to reach order service',
            'details': str(e)
        }), 503

@app.route('/orders/<int:order_id>')
def get_order(order_id):
    stats['total_requests'] += 1
    stats['orders_requests'] += 1
    
    try:
        response = requests.get(f'{ORDER_SERVICE_URL}/orders/{order_id}', timeout=10)
        
        if response.status_code == 404:
            return jsonify({'error': 'Order not found'}), 404
        
        if response.status_code != 200:
            stats['errors'] += 1
            return jsonify({'error': 'Order service error'}), response.status_code
        
        data = response.json()
        data['via'] = 'api-gateway'
        return jsonify(data)
        
    except requests.exceptions.RequestException as e:
        stats['errors'] += 1
        return jsonify({
            'error': 'Failed to reach order service',
            'details': str(e)
        }), 503

@app.route('/users/<int:user_id>/complete')
def get_complete_user_info(user_id):
    stats['total_requests'] += 1
    stats['users_requests'] += 1
    stats['orders_requests'] += 1
    
    try:
        user_response = requests.get(f'{USER_SERVICE_URL}/users/{user_id}', timeout=10)
        
        if user_response.status_code == 404:
            return jsonify({'error': 'User not found'}), 404
        
        if user_response.status_code != 200:
            stats['errors'] += 1
            return jsonify({'error': 'User service error'}), 502
        
        user_data = user_response.json()
        
        orders_response = requests.get(f'{ORDER_SERVICE_URL}/orders/user/{user_id}', timeout=10)
        
        orders_data = {}
        if orders_response.status_code == 200:
            orders_data = orders_response.json()
        else:
            orders_data = {
                'count': 0,
                'total_amount': 0,
                'orders': [],
                'error': 'Could not fetch orders'
            }
        
        complete_data = {
            'via': 'api-gateway',
            'aggregated_from': ['user-service', 'order-service'],
            'user': user_data.get('user', {}),
            'orders_summary': {
                'total_orders': orders_data.get('count', 0),
                'total_spent': orders_data.get('total_amount', 0),
                'orders': orders_data.get('orders', [])
            },
            'timestamp': datetime.now().isoformat()
        }
        
        return jsonify(complete_data)
        
    except requests.exceptions.RequestException as e:
        stats['errors'] += 1
        return jsonify({
            'error': 'Failed to aggregate data',
            'details': str(e)
        }), 503

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    print(f"API Gateway iniciando na porta {port}...")
    print(f"User Service: {USER_SERVICE_URL}")
    print(f"Order Service: {ORDER_SERVICE_URL}")
    app.run(host='0.0.0.0', port=port, debug=True)
