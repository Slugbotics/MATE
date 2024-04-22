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

import time


def main():

    sg.theme("DarkBlack")


    # Define the window layout

    layout = [
        [sg.Image(filename="", key="-IMAGE-"), sg.Image(filename="", key="-IMAGE-"), sg.Image(filename="", key="-IMAGE-")],
        [sg.Image(filename="", key="-IMAGE-"), sg.Image(filename="", key="-IMAGE-"), sg.Image(filename="", key="-IMAGE-")],
        [sg.StatusBar("Network Status"), sg.StatusBar("Last Input Sent")],
        [sg.StatusBar("Thruster 1 status"), sg.StatusBar("Thruster 2 status")],
        [sg.StatusBar("Thruster 3 status"), sg.StatusBar("Thruster 4 status")],
        [sg.Push(), sg.Button("Exit", size=(10, 1))],

    ]



    window = sg.Window("Slugbotics Driver Station", layout, location=(0, 0), resizable=True)
    window.read(timeout=20)
    window.maximize()

    cams = []
    for i in range(0,6):
        cams.append(cv2.VideoCapture(i))
        if not cams[i].isOpened():
            print(f"Camera: {i} failed to capture, skipping")
            continue
        cams[i].set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cams[i].set(cv2.CAP_PROP_FRAME_HEIGHT, 360)
        cams[i].set(cv2.CAP_PROP_FPS, 60)
    # Event loop
    while True:
        event, values = window.read(timeout=20)
        if event == "Exit" or event == sg.WIN_CLOSED:
            break

        for cam in cams:
            ret, frame = cam.read()
            frame = cv2.resize(frame, (640, 360))
            imgbytes = cv2.imencode(".png", frame)[1].tobytes()
            window["-IMAGE-"].update(data=imgbytes)


    window.close()
    for i in range(len(cams)): 
        cv2.VideoCapture(i).release()


if __name__ == "__main__":
    main()
