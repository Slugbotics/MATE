from input import controller
import vec_util

import socket
import time
import math
import logging
import threading

import gui

try: 
    mc = 0
    move_controller = controller(mc)
except IndexError as e:
    print("Error: Driver Controller not connected")
    exit()
try:
    ac = 1
    arm_controller = controller(ac)
except IndexError as e:
    print("Error: operator controller not connected")
#    exit()

# Create logger object
log_format = "%(asctime)s: %(message)s"
logging.basicConfig(filename="topside_rover.log", format=log_format, encoding="utf-8", level=logging.DEBUG, datefmt="%Y-%m-%d %H:%M:%S")

# Direction vectors for each of the corner motors
top_l_direction = (1/math.sqrt(2), 1/math.sqrt(2))
top_r_direction = (-1/math.sqrt(2), 1/math.sqrt(2))
bot_l_direction = (-1/math.sqrt(2), 1/math.sqrt(2))
bot_r_direction = (1/math.sqrt(2), 1/math.sqrt(2))

#client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_addr = "192.168.1.155"
server_port = 8888
#client.bind((server_addr, server_port))
logging.info(f"Binding to {server_addr}:{server_port}")
client_addr = "192.168.1.177"
client_port = 8888

# Start GUI thread
gui = threading.Thread(target=gui.main, args=[move_controller])
gui.start()
logging.info("Starting Driver GUI")

while True:

    translation = move_controller.left_stick
    rotation, v_translation = move_controller.right_stick

    # Normalization and dead zone for directional translation input
    translation_mag = vec_util.magnitude(translation)
    if translation_mag > 1:
        translation = vec_util.div_vec(translation, translation_mag)
    elif translation_mag < 0.1:
        translation = (0, 0)
    else:
        translation = (0, 0)

    # Dead zone for rotation
    if abs(rotation) < 0.1:
        rotation = 0

    # Dead zone for vertical translation
    if abs(v_translation) < 0.1:
        v_translation = 0

    # Get thrust for each motor based on how much it points in the target direction
    front_left = vec_util.dot(top_l_direction, translation) + rotation
    front_right = vec_util.dot(top_r_direction, translation) - rotation
    back_left = vec_util.dot(bot_l_direction, translation) + rotation
    back_right = vec_util.dot(bot_r_direction, translation) - rotation

    # Scale all motor values evenly to keep them from clipping
    max_thrust = max([abs(front_left), abs(front_right), abs(back_left), abs(back_right)])
    if max_thrust > 1:
        front_left /= max_thrust
        front_right /= max_thrust
        back_left /= max_thrust
        back_right /= max_thrust

    # Map thrust values to packet values
    front_left = round(front_left * 50) + 50
    front_right = round(front_right * 50) + 50
    back_left = round(back_left * 50) + 50
    back_right = round(back_right * 50) + 50
    top_front = round(v_translation * 50) + 50
    top_back = round(v_translation * 50) + 50


    #checksum
    checksum = (front_left + front_right + back_left + back_right + top_front + top_back) % 256
    # Create and send packet
    packet = bytearray()
    for field in [checksum, front_left, front_right, back_left, back_right, top_front, top_back]:
        packet.extend(field.to_bytes(1, byteorder="big", signed=False))
#    packet.extend(arm_controller.gen_packet())
    logging.info(f"Sending packet: {packet}")
#    client.sendto(packet, (client_addr, client_port))
    # message, addr = client.recvfrom(2000)
    # logging.info(f"Got message: {message}")
    time.sleep(0.35)
