''' Camera GUI, 

displays one camera in a window
submodule for driver station gui'''

import cv2

import time

window_width = 640
window_height = 360
screen_width = 1920
screen_height = 1080

def display_camera(device_num: int) -> None:
    """Thread function: takes in a camera file location, displays video to ui""" 
    stream_window = f"cam{device_num}" 
    # From Mateusz Bielecki on stackoverflow
    cv2.namedWindow(
        stream_window,
        flags=(cv2.WINDOW_NORMAL | cv2.WINDOW_GUI_NORMAL | cv2.WINDOW_FREERATIO))
    cv2.setWindowProperty(stream_window, cv2.WND_PROP_TOPMOST, 1.0)
    cv2.setWindowProperty(stream_window, cv2.WND_PROP_FULLSCREEN, 1.0)
    cv2.resizeWindow(
        stream_window,
        window_width,
        window_height)
    cv2.moveWindow(
        stream_window,
        screen_width - window_width,
        screen_height - window_height - 40)

    cam = cv2.VideoCapture(device_num)
    if not cam.isOpened():
        print(f"Error: camera {device_num} could not be loaded")
        return -1
    cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
    cam.set(cv2.CAP_PROP_FPS, 30)
    while cv2.waitKey(1) & 0xFF != ord('q'):
        ret, frame = cam.read()
        frame = cv2.resize(frame, (640, 360))
        cv2.imshow(stream_window, frame)
        time.sleep(0.033)
    cam.release()
