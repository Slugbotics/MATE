from input import controller
import socket
import time
import math
import logging

mc = 0
move_controller = controller(mc)
ac = 1
arm_controller = controller(ac)

def div_vec(v : tuple[float, float], n : float) -> tuple[float, float]:
    x, y = v
    return (x / n, y / n)

def magnitude(vec : tuple[float, float]) -> float:
    x, y = vec
    return math.sqrt(x * x + y * y)

def dot(a : tuple[float, float], b : tuple[float, float]) -> float:
    ax, ay = a
    bx, by = b
    return ax * bx + ay * by

# Create logger object
logging.basicConfig(filename="topside_rover.log", encoding="utf-8", level=logging.DEBUG)

# Direction vectors for each of the corner motors
top_l_direction = (1/math.sqrt(2), 1/math.sqrt(2))
top_r_direction = (-1/math.sqrt(2), 1/math.sqrt(2))
bot_l_direction = (-1/math.sqrt(2), 1/math.sqrt(2))
bot_r_direction = (1/math.sqrt(2), 1/math.sqrt(2))

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_addr = "192.168.1.155"
server_port = 8888
client.bind((server_addr, server_port))
logging.info(f"Binding to {server_addr}:{server_port}")

while True:
    translation = controller.left_stick
    rotation, v_translation = controller.right_stick

    BTN_X = controller.x_pressed
    BTN_Y = controller.y_pressed
    BTN_B = controller.b_pressed

    Left_Bumper = controller.btn_tl
    Right_Bumper = controller.btn_tr

    # Normalization and dead zone for directional translation input
    translation_mag = magnitude(translation)
    if translation_mag > 1:
        translation = div_vec(translation, translation_mag)
    elif translation_mag < 0.1:
        translation = (0, 0)

    # Dead zone for rotation
    if abs(rotation) < 0.1:
        rotation = 0

    # Dead zone for vertical translation
    if abs(v_translation) < 0.1:
        v_translation = 0

    # Get thrust for each motor based on how much it points in the target direction
    front_left = dot(top_l_direction, translation) + rotation
    front_right = dot(top_r_direction, translation) - rotation
    back_left = dot(bot_l_direction, translation) + rotation
    back_right = dot(bot_r_direction, translation) - rotation

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
<<<<<<< HEAD
    packet = ", ".join([str(front_left), str(front_right), str(back_left), str(back_right), str(top_front), str(top_back)])
    
=======
    packet = ", ".join([str(front_left), str(front_right), str(back_left), str(back_right), str(top_front), str(top_back),
                         str(BTN_X), str(BTN_Y), str(BTN_B), str(Left_Bumper), str(Right_Bumper)])
    return packet

#Rather than sending two packets, perhaps we have both of the methods add their string array onto the packet itself,
#create a method for the packet and just have the other methods add to the packet
     
while True:
    mc_packet = logic(move_controller)
    ac_packet = logic(arm_controller)

    packet = '['+ str(mc) + ']' + ', ' + mc_packet + ', ' + '[' + str(ac) + ']' + ', ' + ac_packet
    print(packet)
    # client.sendto(mc_packet.encode(), ("192.168.1.177", 8888))
    # client.sendto(ac_packet.encode(), ("192.168.1.177", 8888))
    # message, addr = client.recvfrom(2000)
    #print(message)
>>>>>>> caac142 (jonathan dont delete this branch - accomplished: buttons added to packet & controller packets merged into one string. PS Ananya doesnt know what shes talking about)


    # Create and send packet
    packet = bytearray()
    for field in [checksum, front_left, front_right, back_left, back_right, top_front, top_back]:
        packet.append(field)
    logging.info(f"Sending packet: {packet}")
    client_addr = "192.168.1.177"
    client_port = 8888
    client.sendto(packet.encode(), (client_addr, client_port))
    # message, addr = client.recvfrom(2000)
    # logging.info(f"Got message: {message}")

    time.sleep(0.1)
