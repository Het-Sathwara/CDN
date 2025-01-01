import socket
import threading
import json
import sys

def handle_client(client_socket):
    request = client_socket.recv(1024)
    print(f"Received: {request.decode()}")

    code_response = json.dumps({"type": "code", "content": "print('Hello from server on port {}!')".format(sys.argv[1])})
    client_socket.send(code_response.encode())
    client_socket.close()

def start_server(port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('', port))
    server.listen(5)
    print(f"Server listening on port {port}")

    while True:
        client_socket, addr = server.accept()
        print(f"Accepted connection from {addr}")
        handle_client(client_socket)

if __name__ == "__main__":
    start_server(int(sys.argv[1]))
