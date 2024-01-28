''' Runs the driver station GUI

displays:
- camera / opencv output
- network info
- last input sent

This program will ask for permission to read the webcam (popup)'''

import PySimpleGUI as sg

import cv2

import numpy as np


def main():

    sg.theme("DarkBlack")


    # Define the window layout

    layout = [
        [sg.Image(filename="", key="-IMAGE-")],

        [sg.Button("Exit", size=(10, 1))],

    ]


    # Create the window and show it without the plot

    window = sg.Window("Slugbotics Driver Station", layout, location=(0, 0))

    cap = cv2.VideoCapture(0)

    window_maximized = False
    while True:

        event, values = window.read(timeout=20)

        if not window_maximized:
            window.maximize()
        
        if event == "Exit" or event == sg.WIN_CLOSED:

            break


        ret, frame = cap.read()


        
        imgbytes = cv2.imencode(".png", frame)[1].tobytes()

        window["-IMAGE-"].update(data=imgbytes)


    window.close()


main()
