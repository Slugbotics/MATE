''' Camera GUI, 

displays one camera in a window
submodule for driver station gui'''

import cv2
from vidgear.gears import CamGear
import PySimpleGUI as sg

import time

cam_width = 1280 
cam_height = 720 
# screen_width = 1920
# screen_height = 1080
options = {"CAP_PROP_FPS": 20, 
           "CAP_PROP_FRAME_WIDTH": cam_width, 
           "CAP_PROP_FRAME_HEIGHT": cam_height}

def display_camera(device_num: int, window) -> None:
    """Thread function: takes in a camera file location, displays video to ui""" 
    
    cam = CamGear(source=device_num, **options).start()

    while True:
        frame = cam.read()
        if frame is None:
            break
        imgbytes = cv2.imencode(".png", frame)[1].tobytes()
        window[f"cam"].update(data=imgbytes) 
    cam.stop()
