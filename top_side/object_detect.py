import tkinter as tk
from PIL import Image, ImageTk
import cv2 as cv
import detection

obj = False
hand = False

window = tk.Tk()
vid = cv.VideoCapture(0)

window.rowconfigure(0, minsize=100)
window.columnconfigure([0,1], minsize=200)

if not vid.isOpened():
    print("Camera cant be opened")
    exit()

buttons = tk.Frame(master=window)
buttons.grid(row=0, column=0)

def object_method():
    global obj
    obj = not obj
def hand_method():
    global hand
    hand = not hand

button1 = tk.Button(master=buttons, text="Object Detection", command=object_method)
button1.pack(padx=20, pady=5)

button2 = tk.Button(master=buttons, text="Hand Detection", command=hand_method)
button2.pack(padx=20, pady=5)
# buttons.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)
def get_cam():
    _, frame = vid.read()

    opencv_img = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    copy = cv.cvtColor(frame, cv.COLOR_BGR2RGB)

    if obj:
        detection.write_marks_detection(opencv_img, copy)
    if hand:
        detection.write_marks_hands(opencv_img, copy)
    
    img = ImageTk.PhotoImage(image=Image.fromarray(copy))

    return img

img_container = tk.Label(image=get_cam())
img_container.grid(row=0, column=1)

def set_img():
    img = get_cam()
    img_container.photo_image = img
    img_container.configure(image=img)
    img_container.after(20, set_img)


set_img()
window.mainloop()
vid.release()
cv.destroyAllWindows()