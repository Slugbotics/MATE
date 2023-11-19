import socket

def run_client():
    
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    server_ip = "169.233.179.96"
    #Get ip value later
    server_port = 1222

    client.connect((server_ip, server_port))
    print("connected to server")

    while True:
        msg = input("Enter message: ")
        client.send(msg.encode("utf-8")[:1024])
        
        response = client.recv(1024)
        response = response.decode("utf-8")

        if response.lower() == "closed":
            break

        print(f'Received: {response}')

    client.close()
    print("Connection to server closed")

run_client()


