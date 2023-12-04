import socket
import time

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
print("socket created")

<<<<<<< HEAD
port = 12345
=======
port = 1222
>>>>>>> 7d29bd53371b139b9ed384f07bcbe1c4413b0b1f
server = ''
s.bind((server, port))
print("socket binded to %s" %(port))


while True:
    data, addr = s.recvfrom(1024)
    print("received data:", data.decode("utf-8"))  
    
    msg = input("Enter message: ")
    # s.send(msg.encode("utf-8")[:1024])
    s.sendto(msg.encode("utf-8"), addr)






