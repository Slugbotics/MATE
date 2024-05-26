''' Runs the driver station GUI

displays:
- camera / opencv output
- network info

'''

import PySimpleGUI as sg

import camera_gui


def main(controller) -> None:
    cams = []
    # Place each camera index on each new line in top_side/cams.txt
    # order of cams, front, left, right, back
    with open("cams.txt", "r") as cam_file:
        cams = [int(x) for x in cam_file]
    curr_device_num = cams[0]

    sg.theme("DarkBlack")

    layout = [
        [sg.Push(), sg.Text("Current Camera: "), sg.Text("", key="-CAM_NUM-"), sg.Push()],
        [sg.Push(), sg.Image(filename="", key="cam"), sg.Push()],
        [sg.StatusBar("Network Status"), sg.StatusBar("Last Input Sent")],
        [sg.StatusBar("Thruster 1 status"), sg.StatusBar("Thruster 2 status")],
        [sg.StatusBar("Thruster 3 status"), sg.StatusBar("Thruster 4 status")],
        [sg.Push(), sg.Button("Exit", size=(10, 1))]
    ]

    window = sg.Window("Slugbotics Driver Station", layout, location=(0, 0), size=(1920, 1080))
    feed = camera_gui.CameraFeed(window, controller)
    feed.enable()
    window.start_thread(lambda: feed.run(), ("", ""))


    # Event loop
    while True:
        event, values = window.read()
        if event in ("Exit", sg.WIN_CLOSED):
            break

    feed.disable()
    del feed
    window.close()
 

