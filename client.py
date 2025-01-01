import socket
import json

def request_content(load_balancer_ip, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((load_balancer_ip, port))
        s.sendall(b"GET / HTTP/1.1\r\nHost: localhost\r\n\r\n")
        response = s.recv(4096)

        response_data = json.loads(response.decode())
        
        if response_data['type'] == 'code':
            exec(response_data['content'])  
        else:
            print(response_data['content'])

if __name__ == "__main__":
    request_content('127.0.0.1', 33000)  