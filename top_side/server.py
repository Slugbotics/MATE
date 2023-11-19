import socket

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
print("socket created")

port = 1222
server = ''
s.bind((server, port))
print("socket binded to %s" %(port))

while True:
    data, addr = s.recvfrom(1024)
    print("received data ", data)  





