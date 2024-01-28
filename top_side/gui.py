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

    sg.theme("LightGreen")


    # Define the window layout

    layout = [

        [sg.Text("Slugbotics Driver Station", size=(60, 1), justification="center")],

        [sg.Image(filename="", key="-IMAGE-")],

        [sg.Button("Exit", size=(10, 1))],

    ]


    # Create the window and show it without the plot

    window = sg.Window("OpenCV Integration", layout, location=(800, 400))


    cap = cv2.VideoCapture(0)


    while True:

        event, values = window.read(timeout=20)

        if event == "Exit" or event == sg.WIN_CLOSED:

            break


        ret, frame = cap.read()


        
        imgbytes = cv2.imencode(".png", frame)[1].tobytes()

        window["-IMAGE-"].update(data=imgbytes)


    window.close()


main()
