import socket
import time

def load_balancer(servers, port):
    while True:
        for server in servers:
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.connect((server, port))
                    print(f"Connected to server: {server}")
                    return server
            except Exception as e:
                print(f"Server {server} is down: {e}")
        time.sleep(5)

if __name__ == "__main__":
    
    servers = [('127.0.0.1', 33000), ('127.0.0.1', 33001), ('127.0.0.1', 33002)]
    selected_server = load_balancer(servers, 33000)
