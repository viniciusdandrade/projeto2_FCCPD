from flask import Flask, jsonify
from datetime import datetime, timedelta
import random

app = Flask(__name__)

ORDERS_DB = [
    {'id': 1, 'user_id': 1, 'product': 'Laptop', 'amount': 2500.00, 'status': 'delivered', 'date': '2025-10-15'},
    {'id': 2, 'user_id': 1, 'product': 'Mouse', 'amount': 50.00, 'status': 'delivered', 'date': '2025-10-20'},
    {'id': 3, 'user_id': 2, 'product': 'Keyboard', 'amount': 150.00, 'status': 'shipped', 'date': '2025-11-01'},
    {'id': 4, 'user_id': 3, 'product': 'Monitor', 'amount': 800.00, 'status': 'processing', 'date': '2025-11-10'},
    {'id': 5, 'user_id': 4, 'product': 'Webcam', 'amount': 300.00, 'status': 'delivered', 'date': '2025-11-15'},
    {'id': 6, 'user_id': 5, 'product': 'Headset', 'amount': 200.00, 'status': 'shipped', 'date': '2025-11-18'},
    {'id': 7, 'user_id': 1, 'product': 'USB Hub', 'amount': 75.00, 'status': 'delivered', 'date': '2025-11-20'}
]

@app.route('/')
def home():
    return jsonify({
        'service': 'Order Service',
        'version': '1.0.0',
        'description': 'Gerenciamento de pedidos',
        'endpoints': {
            '/orders': 'Lista todos os pedidos',
            '/orders/<id>': 'Detalhes de um pedido',
            '/orders/user/<user_id>': 'Pedidos de um usuário'
        }
    })

@app.route('/health')
def health():
    return jsonify({'status': 'healthy', 'service': 'order-service'})

@app.route('/orders')
def get_orders():
    return jsonify({
        'service': 'order-service',
        'timestamp': datetime.now().isoformat(),
        'count': len(ORDERS_DB),
        'orders': ORDERS_DB
    })

@app.route('/orders/<int:order_id>')
def get_order(order_id):
    order = next((o for o in ORDERS_DB if o['id'] == order_id), None)
    if not order:
        return jsonify({'error': 'Order not found'}), 404
    return jsonify({
        'service': 'order-service',
        'order': order
    })

@app.route('/orders/user/<int:user_id>')
def get_user_orders(user_id):
    user_orders = [o for o in ORDERS_DB if o['user_id'] == user_id]
    total_amount = sum(o['amount'] for o in user_orders)
    
    return jsonify({
        'service': 'order-service',
        'user_id': user_id,
        'count': len(user_orders),
        'total_amount': total_amount,
        'orders': user_orders
    })

if __name__ == '__main__':
    print("Order Service iniciando na porta 5002...")
    app.run(host='0.0.0.0', port=5002, debug=True)
