from flask import Flask, jsonify
from datetime import datetime
import os

app = Flask(__name__)

request_count = 0

@app.route('/')
def home():
    global request_count
    request_count += 1
    return jsonify({
        'message': 'Servidor Flask funcionando!',
        'timestamp': datetime.now().isoformat(),
        'hostname': os.uname().nodename,
        'request_number': request_count
    })

@app.route('/health')
def health():
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat()
    })

if __name__ == '__main__':
    print("Servidor iniciando na porta 8080...")
    app.run(host='0.0.0.0', port=8080, debug=True)
