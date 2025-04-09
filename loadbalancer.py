from flask import Flask, jsonify
import requests
from itertools import cycle
import threading
import time
from flask import Flask, jsonify, request
from flask_cors import CORS  # Add this import

app = Flask(__name__)
CORS(app) 

servers = ['http://localhost:33000', 'http://localhost:33001', 'http://localhost:33002']
active_servers = []
server_pool = cycle(servers)

def health_check():
    global active_servers
    while True:
        healthy = []
        for server in servers:
            try:
                response = requests.get(f"{server}/health", timeout=2)
                if response.status_code == 200:
                    healthy.append(server)
            except:
                pass
        active_servers = healthy
        time.sleep(5)

@app.route('/')
def router():
    if not active_servers:
        return "No healthy servers available", 503
        
    for _ in range(len(active_servers)):
        server = next(server_pool)
        if server in active_servers:
            try:
                response = requests.get(server)
                return response.content
            except:
                continue
    return "All servers are busy", 503

@app.route('/servers')
def get_servers():
    return jsonify([{
        'url': server,
        'port': server.split(':')[-1],
        'upload_url': f"{server}/upload"
    } for server in active_servers])

if __name__ == '__main__':
    threading.Thread(target=health_check, daemon=True).start()
    app.run(port=8080)