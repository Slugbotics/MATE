import tkinter as tk

clicks = 0

def click():
    global clicks
    clicks += 1
    if clicks == 10:
        button.configure(text=":P")

root = tk.Tk()
root.title("ROV GUI")
frame = tk.Frame(root, padx=50, pady=50)
frame.pack(expand=True)
label = tk.Label(frame, text="Nothing to see here YET...")
label.grid(row=0, column=0)
button = tk.Button(frame, text="But you can click anyway", command=click)
button.grid(row=1, column=0)
root.mainloop()