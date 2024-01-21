import input
import socket
import time
import math

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

client.bind(("192.168.1.155", 8888))

while True:
    top_l = (1/math.sqrt(2), 1/math.sqrt(2))
    top_r = (-1/math.sqrt(2), 1/math.sqrt(2))
    bot_l = (-1/math.sqrt(2), 1/math.sqrt(2))
    bot_r = (1/math.sqrt(2), 1/math.sqrt(2))

    input_x, input_y = input.left_stick

    magnitude = math.sqrt(input_x ** 2 + input_y ** 2)

    if magnitude > 1:
        input_x = input_x / magnitude
        input_y = input_y / magnitude

    top_left = top_l[0] * input_x + top_l[1] * input_y
    top_right = top_r[0] * input_x + top_r[1] * input_y
    bot_left = bot_l[0] * input_x + bot_l[1] * input_y
    bot_right = bot_r[0] * input_x + bot_r[1] * input_y
    
    packet = str(top_left) + ", " + str(top_right) + ", " + str(bot_left) + ", " + str(bot_right)
    client.sendto(packet.encode(), ("192.168.1.177", 8888))
    message, addr = client.recvfrom(2000)
    print(message)

    time.sleep(0.1)