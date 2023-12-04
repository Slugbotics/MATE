import socket
import time

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
print("socket created")

port = 12345
server = ''
s.bind((server, port))
print("socket binded to %s" %(port))


while True:
    data, addr = s.recvfrom(1024)
    print("received data:", data.decode("utf-8"))  
    
    msg = input("Enter message: ")
    # s.send(msg.encode("utf-8")[:1024])
    s.sendto(msg.encode("utf-8"), addr)






