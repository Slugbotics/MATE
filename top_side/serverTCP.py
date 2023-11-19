import socket

PORT = 5051

# IPv4
# SERVER = "169.233.155.123"

# Alternate way to get the IPv4
SERVER = socket.gethostbyname(socket.gethostname())
# SERVER = "192.168.1.177"

ADDR = (SERVER, PORT)
FORMAT = "utf-8"

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind(ADDR)

print(socket.gethostname())  # gets the host name


def start():
    print(f"[LISTENING] Server is listening on {SERVER}")

    while True:
        data, addr = server.recvfrom(1024)  # buffer size is 1024 bytes

        # You can modify this part according to your needs
        msg = data.decode(FORMAT)
        print(f"[{addr}] {msg}")

        # You can add your server logic here to process the received message
        # ...


print("[STARTING] server is starting...")
start()
