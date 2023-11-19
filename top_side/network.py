# basic file for understanding socket connection
# importing the module
import socket
# creating a socket and connection between the devices --> sock-stream is a connection oriented TCP
s1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
print("sockets successfully created")

port = 80
host_ip = socket.gethostbyname("www.google.com")
s1.connect((host_ip, port))
print("the socket has connected to google")
