import socket

def run_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_ip = "0.0.0.0"
    port = 8000
    server.bind((server_ip, port))
    server.listen(1)
    print(f"listening on {server_ip}:{port}")
    client_socket, client_address = server.accept()
    print(f"accepted connection from {client_address[0]}:{client_address[1]}")

    request = client_socket.recv(1024)
    request = request.decode("utf-8")

    print(f"Received: {request}")
    response = "accepted".encode("utf-8")
    client_socket.send(response)

    client_socket.close()
    print("connection to client closed")
    server.close()

def send_file():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_ip = "0.0.0.0"
    port = 8000
    server.bind((server_ip, port))
    server.listen(1)
    print(f"listening on {server_ip}:{port}")
    client_socket, client_address = server.accept()
    print(f"accepted connection from {client_address[0]}:{client_address[1]}")

    filename = "float_data.txt"
    client_socket.send(filename.encode("utf-8"))
    print(f"Sent: {filename}")
    file = open(filename, "r")
    data = file.read()
    client_socket.send(data.encode("utf-8"))
    print(f"Sent: {data}")
    file.close()
    client_socket.close()
    print("connection to client closed")
    server.close()

def receive_file():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_ip = "100.64.60.135"
    server_port = 8000
    client.connect((server_ip, server_port))

    filename = client.recv(1024).decode("utf-8")
    print(f"Received: {filename}")
    file = open(filename, "w")

    data = client.recv(1024).decode("utf-8")
    print(f"[RECV] Receiving the file data.")
    file.write(data)
    client.send("File data received".encode("utf-8"))

    file.close()
    client.close()
    print("connection to server closed")

send_file()