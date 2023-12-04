import socket

def run_client():
    
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    server_ip = socket.gethostbyname(socket.gethostname())
    # get ip address of server
    server_port = 12543

    client.connect((server_ip, server_port))
    print("connected to server")

    while True:
        msg = input("Enter message: ")
        client.send(msg.encode("utf-8")[:1024])
        
        response, addr = client.recvfrom(1024)
        response = response.decode("utf-8")

        if response.lower() == "closed":
            break

        print(f'Received: {response}')

    client.close()
    print("Connection to server closed")

run_client()


