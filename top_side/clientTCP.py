import socket

PORT = 5051
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = socket.gethostbyname(socket.gethostname())
# SERVER = "192.168.1.177"
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


def send(msg):
    message = msg.encode(FORMAT)
    client.sendto(message, ADDR)


send("Hello World")
input()
send("Hello 2")
input()
send("Hello 3")
send(DISCONNECT_MESSAGE)
