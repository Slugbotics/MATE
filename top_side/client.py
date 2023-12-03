# importing the module
import socket
# creating a socket and connection between the devices --> sock-stream is a connection oriented TCP
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client.sendto(b"Hello!", ("192.168.1.177", 8888))