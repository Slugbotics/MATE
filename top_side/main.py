import input
import time
import math

#while True:
#    print(str(input.left_stick) + " " + str(input.right_stick) + " " + str(input.x_pressed))
#    time.sleep(0.1)

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
    
    print(f'Top Left: {top_left}, Top Right: {top_right}, Bottom Left: {bot_left}, Bottom Right: {bot_right}')

    #print(str(input.left_stick) + " " + str(input.right_stick) + " " + str(input.x_pressed))
    time.sleep(0.1)