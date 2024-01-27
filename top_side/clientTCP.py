import socket

PORT = 5051
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


def send(msg):
    # encode and send a message to the server
    message = msg.encode(FORMAT)
    client.sendto(message, ADDR)

    # (if needed) receive and decode a message from the server
    print(client.recvfrom(1024)[0].decode(FORMAT))
    


send("Hello World")
input()
send("Hello 2")
input()
send("Hello 3")
send("END")