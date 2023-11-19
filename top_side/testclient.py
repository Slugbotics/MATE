import socket

HEADER = 64
PORT = 5050
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = socket.gethostbyname(socket.gethostname())
SERVER = "192.168.1.177"
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client.connect(ADDR)



def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)

    # need to subtract 64 by str(msg_length).encode(FORMAT)
    # that will figure how much to pad the message so it is the length 64

    send_length += b' ' * (HEADER-len(send_length)) #b' ' adds blank spaces
    client.send(send_length)
    client.send(message)

send("Hello World")
input()
send("Hello 2")
input()
send("Hello 3")
send(DISCONNECT_MESSAGE)