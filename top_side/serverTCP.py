import socket

PORT = 5051

# IPv4
# SERVER = "169.233.155.123"

# Alternate way to get the IPv4 dynamically
SERVER = socket.gethostbyname(socket.gethostname())

ADDR = (SERVER, PORT)
FORMAT = "utf-8"

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind(ADDR)

print(socket.gethostname())  # gets the host name


def start():
    print(f"[LISTENING] Server is listening on {SERVER}")

    while True:

        # we don't call server.listen() because we don't listen for connections only messages
        # here we would use .recvfrom() : meaning receive from
        # it gives us the message/data as well as the address 

        # if we need more buffer size we can change to avoid dropping messages 
        data, addr = server.recvfrom(1024) 
        
        # here we are checking that we can get the messages from the client
        msg = data.decode(FORMAT)
        print(f"[{addr}] {msg}")

        # (if needed) test that we can send messages back to the client
        server.sendto("Hello client".encode(FORMAT), addr)




print("[STARTING] server is starting...")
start()
