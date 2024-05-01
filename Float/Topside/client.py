import socket

def run_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_ip = "100.64.60.135"
    server_port = 8000
    client.connect((server_ip, server_port))

    while True:
        msg = input("enter message: ")
        client.send(msg.encode("utf-8"))
        response = client.recv(1024)
        response = response.decode("utf-8")
       
        if response.lower() == "closed":
            break

        print(f"received: {response}")
    
    client.close()
    print("connection to server closed")

run_client()