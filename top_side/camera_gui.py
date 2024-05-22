''' Camera GUI, 

displays one camera in a window
submodule for driver station gui'''

import cv2
from vidgear.gears import CamGear
import PySimpleGUI as sg

import time

class CameraFeed:
    def __init__(self, window, controller):
        """takes controller to switch cameras"""
        self.window = window
        self.controller = controller

        # Place each camera index on each new line in top_side/cams.txt
        # order of cams, front, left, right, back
        with open("cams.txt", "r") as cam_file:
            self.cams = [int(x) for x in cam_file]

        print(self.cams)

        cam_width = 640 
        cam_height = 360 
        self.options = {"CAP_PROP_FPS": 30, 
                   "CAP_PROP_FRAME_WIDTH": 1280, 
                   "CAP_PROP_FRAME_HEIGHT": 720}


        self.running = False

    def __del__(self):
        try:
            self.cam.stop()
        except Exception as e:
            print("WARN: Tried to stop cam, couldnt")

    def get_device(self):
        return self.cams[self.controller.curr_cam]

    def enable(self):
        self.running = True

    def disable(self):
        self.running = False

    def setup_cam(self):
        self.cam = CamGear(source=self.get_device(), **self.options)
        self.window["-CAM_NUM-"].update(self.controller.curr_cam)
        self.cam.start()

    def run(self) -> None:
        self.setup_cam()
        curr_cam = self.get_device()
        while self.running:
            if curr_cam != self.get_device():
                print("RESETING CAMERA FEED")
                self.cam.stop()
                self.setup_cam()
                curr_cam = self.get_device()
             
            frame = self.cam.read()
            if frame is None:
                time.sleep(0.012)
                       
            imgbytes = cv2.imencode(".png", frame)[1].tobytes()
            self.window[f"cam"].update(data=imgbytes) 
