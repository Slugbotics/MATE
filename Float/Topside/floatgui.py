import PySimpleGUI as sg
import pygal
import io
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM
from PIL import Image
import time
import socket

def send_ip():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_ip = "192.168.4.1"
    server_port = 5000
    client.connect((server_ip, server_port))

    data = "ip " + socket.gethostbyname(socket.gethostname())
    print(data)
    client.send(data.encode("utf-8"))
    print(data)
    response = client.recv(1024)
    response = response.decode("utf-8")
       
    if response.lower() == "closed":
        print(f"received: {response}")
    
    client.close()
    print("connection to server closed")

def send_down():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_ip = "192.168.4.1"
    server_port = 5000
    client.connect((server_ip, server_port))
    
    client.send("down".encode("utf-8"))
    response = client.recv(1024)
    response = response.decode("utf-8")
       
    if response.lower() == "closed":
        print(f"received: {response}")
    
    client.close()
    print("connection to server closed")

def receive_file():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_ip = "192.168.4.1"
    server_port = 5000
    client_socket.connect((server_ip, server_port))

    filetodown = open("float_data.txt", "wb+")
    file_content = client_socket.recv(20)
    while True:
        while (file_content):
            filetodown.write(file_content)
            file_content = client_socket.recv(20)
            print(file_content)
        filetodown.close()
        data = client_socket.recv(20)
        if data == b"RECEIVED":
            print("Done Receiving")
            break
    client_socket.close()

def send_time(data):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_ip = "192.168.4.1"
    server_port = 5000
    client.connect((server_ip, server_port))
    
    data = "rtc " + data 
    client.send(data.encode("utf-8"))
    response = client.recv(1024)
    response = response.decode("utf-8")
       
    if response.lower() == "closed":
        print(f"received: {response}")
    
    client.close()
    print("connection to server closed")

def graph_depth(data, time):
    if len(data) != len(time):
        raise Exception("Depth data is mismatched")
    # Generate the depth graph
    depth_graph = pygal.Line()
    depth_graph.title = "Depth over time" 
    depth_graph.x_labels = time
    depth_graph.x_title = "UTC time"
    depth_graph.y_title = "Depth (meters)"
    depth_graph.add("Depth", data)
    depth_graph.render_to_png("depth_graph.png")
    return depth_graph.render(is_unicode=True)
def table_depth(data, time):
    line_chart = pygal.Bar()
    line_chart.title = 'Pressure/Time Table'
    # line_chart.add('time', time)
    line_chart.add('pressure',data)
    line_chart.render_table()
    line_chart.render_to_png("depth_table.png")
def convert_pressure(pressure: float) -> float:
    """Use the hydrostatic pressure equation to convert pressure to depth"""
    density = 0.992720 # kg / m^3 
    pressure = pressure * 100 # hPa -> Pa
    gravity = 9.81 # m / s^2

    return pressure / (density * gravity) 
layout = [
    [sg.Text('Test', text_color='white')],
    [
        sg.Button('Generate Depth Graph', size=(20, 2), button_color=('white', 'black'), font=('Helvetica', 12), key='-GENERATE-', border_width=0 , pad=((0, 10), (10, 10))),
        sg.Button('Exit', size=(10, 2), button_color=('white', 'black'), font=('Helvetica', 12), key='-EXIT-', border_width=0 , pad=((0, 10), (10, 10))),
        sg.Button('time', size=(10, 2), button_color=('white', 'black'), font=('Helvetica', 12), key='-Time-', border_width=0 , pad=((0, 10), (10, 10))),
        sg.Button('Generate Table', size=(10, 2), button_color=('white', 'black'), font=('Helvetica', 12), key='-Table-', border_width=0 , pad=((0, 10), (10, 10))),
        sg.Button('Down', size=(10, 2), button_color=('white', 'black'), font=('Helvetica', 12), key='-Down-', border_width=0 , pad=((0, 10), (10, 10))),
        sg.Button('IP', size=(10, 2), button_color=('white', 'black'), font=('Helvetica', 12), key='-Ip-', border_width=0 , pad=((0, 10), (10, 10)))
    ],
    [sg.Image(key='-IMAGE-')],[sg.Table(values=[], headings=['time','depth'], key="-TBL1-", visible=False,auto_size_columns=True,display_row_numbers=False,justification='center',expand_x=True,
   expand_y=True,)]
]

sg.theme_background_color('black')  # Setting the overall theme background color to black
window = sg.Window('Window', layout, no_titlebar=False, location=(0,0), size=(1200,1600), keep_on_top=True, background_color='black')

while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED or event == '-EXIT-':
        break
    elif event == '-GENERATE-':
        with open("test_output.txt") as file:
            # Read the lines
            lines = file.readlines()
            split = []
            depth_data = []
            time2 = []
            i = 0
            for line in lines:
                split.append(line.split('_'))
            while i < len(split):
                time2.append((split[i][0]))
                depth_data.append(float(split[i][1]))
                i += 1
            i=0
            for o in depth_data:
                depth_data[i] = convert_pressure(o)
                i += 1
            print(depth_data)
            print(time2)
            graph_depth(depth_data, time2)
            image = Image.open('depth_graph.png')
            image.thumbnail((1000, 1000))  # Resize the image if needed
            png_data = io.BytesIO()
            image.save(png_data, format="PNG")
            window['-IMAGE-'].update(data=png_data.getvalue(),visible=True)
            window['-TBL1-'].update(visible = False)
    elif event == '-Time-':
        time1 = str(time.localtime())
        send_time(time1)
    elif event == '-Down-':
        down = 'Down'
        send_down()
    elif event == '-Ip-':
        send_ip()
    elif event == '-Table-':
        with open("test_output.txt") as file:
            # Read the lines
            lines = file.readlines()
            split = []
            depth_data = []
            time2 = []
            i = 0
            for line in lines:
                split.append(line.split('_'))
            while i < len(split):
                time2.append((split[i][0]))
                depth_data.append(float(split[i][1]))
                i += 1
            i=0
            for o in depth_data:
                depth_data[i] = convert_pressure(o)
                i += 1
            for x in split:
                x[1] = convert_pressure(float(x[1]))
            
            window["-IMAGE-"].update(data=None)
            window["-TBL1-"].update(values=split,visible = True)


window.close()