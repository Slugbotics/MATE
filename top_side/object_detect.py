import tkinter as tk
from PIL import Image, ImageTk
import cv2 as cv
import detection

obj = False
hand = False

vid = cv.VideoCapture(0)


if not vid.isOpened():
    print("Camera cant be opened")
    exit()


def object_method():
    global obj
    obj = not obj
def hand_method():
    global hand
    hand = not hand


def get_cam():
    _, frame = vid.read()

    opencv_img = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    copy = cv.cvtColor(frame, cv.COLOR_BGR2RGB)

    if obj:
        detection.write_marks_detection(opencv_img, copy)
    if hand:
        detection.write_marks_hands(opencv_img, copy)
    


    return img



vid.release()
cv.destroyAllWindows()
