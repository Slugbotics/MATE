''' Runs the driver station GUI

displays:
- camera / opencv output
- network info
- last input sent
- thruster data

This program will ask for permission to read the webcam (popup)'''

import PySimpleGUI as sg
import cv2
import numpy as np

import glob
import time
import multiprocessing as mp

import camera_gui

def main() -> None:

    sg.theme("DarkBlack")

    layout = [
        [sg.StatusBar("Network Status"), sg.StatusBar("Last Input Sent")],
        [sg.StatusBar("Thruster 1 status"), sg.StatusBar("Thruster 2 status")],
        [sg.StatusBar("Thruster 3 status"), sg.StatusBar("Thruster 4 status")],
        [sg.Push(), sg.Button("Exit", size=(10, 1))],

    ]


    window = sg.Window("Slugbotics Driver Station", layout, location=(0, 0), no_titlebar=True, size=(1920, 1080))
    window.read()
    time.sleep(1)    

    cams = []
    for i in range(1):
        cams.append(mp.Process(target=camera_gui.display_camera(i)))
        cams[i].start()

    # Event loop
    while True:
        event, values = window.read(timeout=20)
        if event == "Exit" or event == sg.WIN_CLOSED:
            break

    window.close()

 
if __name__ == "__main__":
    main()
