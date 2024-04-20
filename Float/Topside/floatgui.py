import PySimpleGUI as sg
import pygal
import io
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM
from PIL import Image
import time

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
        sg.Button('Generate Table', size=(10, 2), button_color=('white', 'black'), font=('Helvetica', 12), key='-Table-', border_width=0 , pad=((0, 10), (10, 10)))
    ],
    [sg.Image(key='-IMAGE-')]
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
            # Extract depth data and time
            # depth_data = list(map(float, lines[0].split('_')))
            # time2 = list(map(float, lines[1].split('_')))
            # Generate the graph
            graph_depth(depth_data, time2)
            # drawing = svg2rlg("depth_graph.svg")
            # renderPM.drawToFile(drawing, "output.png", fmt="PNG")
            # Update the Image element with the PNG data
            image = Image.open('depth_graph.png')
            image.thumbnail((400, 400))  # Resize the image if needed
            png_data = io.BytesIO()
            image.save(png_data, format="PNG")
            window.close()
            layout = [
            [sg.Text('Test', text_color='white')],
            [
            sg.Button('Generate Depth Graph', size=(20, 2), button_color=('white', 'black'), font=('Helvetica', 12), key='-GENERATE-', border_width=0 , pad=((0, 10), (10, 10))),
            sg.Button('Exit', size=(10, 2), button_color=('white', 'black'), font=('Helvetica', 12), key='-EXIT-', border_width=0 , pad=((0, 10), (10, 10))),
            sg.Button('time', size=(10, 2), button_color=('white', 'black'), font=('Helvetica', 12), key='-Time-', border_width=0 , pad=((0, 10), (10, 10))),
            sg.Button('Generate Table', size=(10, 2), button_color=('white', 'black'), font=('Helvetica', 12), key='-Table-', border_width=0 , pad=((0, 10), (10, 10)))
            ],
            [sg.Image(key='-IMAGE-')]
            ]
            window = sg.Window('Window', layout, no_titlebar=False, location=(0,0), size=(1200,1600), keep_on_top=True, background_color='black', finalize = True)
            window['-IMAGE-'].update(data=png_data.getvalue())
    elif event == '-Time-':
        time1 = time.localtime()
        print(time1)
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
            tbl1 = sg.Table(values=split, headings=['time','depth'],auto_size_columns=True,display_row_numbers=False,justification='center', key='-TABLE-',expand_x=True,
   expand_y=True,)
            layout = [[sg.Text('Test', text_color='white')],
            [
            sg.Button('Generate Depth Graph', size=(20, 2), button_color=('white', 'black'), font=('Helvetica', 12), key='-GENERATE-', border_width=0 , pad=((0, 10), (10, 10))),
            sg.Button('Exit', size=(10, 2), button_color=('white', 'black'), font=('Helvetica', 12), key='-EXIT-', border_width=0 , pad=((0, 10), (10, 10))),
            sg.Button('time', size=(10, 2), button_color=('white', 'black'), font=('Helvetica', 12), key='-Time-', border_width=0 , pad=((0, 10), (10, 10))),
            sg.Button('Generate Table', size=(10, 2), button_color=('white', 'black'), font=('Helvetica', 12), key='-Table-', border_width=0 , pad=((0, 10), (10, 10)))
            ],
            [tbl1],[sg.Image(key='-IMAGE-')]]
            window.close()
            window = sg.Window('Window', layout, no_titlebar=False, location=(0,0), size=(1200,1600), keep_on_top=True, background_color='black')


window.close()