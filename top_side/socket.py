# importing the module
import socket
# creating a socket and connection between the devices --> sock-stream is a connection oriented TCP
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("socket successfully created")
