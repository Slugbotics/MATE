''' Camera GUI, 

displays one camera in a window
submodule for driver station gui'''

import cv2
import PySimpleGUI as sg

import time

window_width = 640
window_height = 360
# screen_width = 1920
# screen_height = 1080

def display_camera(device_num: int, window) -> None:
    """Thread function: takes in a camera file location, displays video to ui""" 
    
    cam = cv2.VideoCapture(device_num)
    if not cam.isOpened():
        print(f"Error: camera {device_num} could not be loaded")
        return -1

    cam.set(cv2.CAP_PROP_FRAME_WIDTH, window_width)
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT, window_height)
    cam.set(cv2.CAP_PROP_FPS, 60)

    while True:
        ret, frame = cam.read()
        imgbytes = cv2.imencode(".png", frame)[1].tobytes()
        window[f"cam{device_num}"].update(data=imgbytes)
    cam.release()
