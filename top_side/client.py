# importing the module
import socket
import input
import time

# creating a socket and connection between the devices --> sock-stream is a connection oriented TCP
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:
    packet = str(input.left_stick) + " " + str(input.right_stick) + " " + str(input.x_pressed)
    client.sendto(packet.encode(), ("192.168.1.177", 8888))
    time.sleep(0.1)