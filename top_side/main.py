import input
import socket
import time
import math

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

# Direction vectors for each of the corner motors
top_l_direction = (1/math.sqrt(2), 1/math.sqrt(2))
top_r_direction = (-1/math.sqrt(2), 1/math.sqrt(2))
bot_l_direction = (-1/math.sqrt(2), 1/math.sqrt(2))
bot_r_direction = (1/math.sqrt(2), 1/math.sqrt(2))

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client.bind(("192.168.1.155", 8888))

while True:
    translation = input.left_stick
    rotation, v_translation = input.right_stick

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
    top_left = dot(top_l_direction, translation) + rotation
    top_right = dot(top_r_direction, translation) - rotation
    bot_left = dot(bot_l_direction, translation) + rotation
    bot_right = dot(bot_r_direction, translation) - rotation

    # Scale all motor values evenly to keep them from clipping 
    max_thrust = max([abs(top_left), abs(top_right), abs(bot_left), abs(bot_right)])
    if max_thrust > 1:
        top_left /= max_thrust
        top_right /= max_thrust
        bot_left /= max_thrust
        bot_right /= max_thrust

    # Map thrust values to packet values
    top_left = round(top_left * 100)
    top_right = round(top_right * 100)
    bot_left = round(bot_left * 100)
    bot_right = round(bot_right * 100)
    top_front = round(v_translation * 100)
    top_back = round(v_translation * 100)

    # Create and send packet
    packet = ", ".join([str(top_left), str(top_right), str(bot_left), str(bot_right), str(top_front), str(top_back)])
    client.sendto(packet.encode(), ("192.168.1.177", 8888))
    message, addr = client.recvfrom(2000)
    print(message)

    time.sleep(0.1)