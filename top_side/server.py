# importing the module
import socket
# creating a socket and connection between the devices --> sock-stream is a connection oriented TCP
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("127.0.0.1", 8080))
server.listen()
print("Listening...")

while True:
    client, addr = server.accept()
    print("Connection from " + str(addr))
