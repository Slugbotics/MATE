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

layout = [
    [sg.Text('Test', text_color='white')],
    [
        sg.Button('Generate Depth Graph', size=(20, 2), button_color=('white', 'black'), font=('Helvetica', 12), key='-GENERATE-', border_width=0 , pad=((0, 10), (10, 10))),
        sg.Button('Exit', size=(10, 2), button_color=('white', 'black'), font=('Helvetica', 12), key='-EXIT-', border_width=0 , pad=((0, 10), (10, 10))),
        sg.Button('time', size=(10, 2), button_color=('white', 'black'), font=('Helvetica', 12), key='-Time-', border_width=0 , pad=((0, 10), (10, 10)))
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
        with open("float_data.txt") as file:
            # Read the lines
            lines = file.readlines()
            # Extract depth data and time
            depth_data = list(map(float, lines[0].split()))
            time2 = list(map(float, lines[1].split()))
            # Generate the graph
            graph_depth(depth_data, time)
            # drawing = svg2rlg("depth_graph.svg")
            # renderPM.drawToFile(drawing, "output.png", fmt="PNG")
            # Update the Image element with the PNG data
            image = Image.open('depth_graph.png')
            image.thumbnail((400, 400))  # Resize the image if needed
            png_data = io.BytesIO()
            image.save(png_data, format="PNG")
            window['-IMAGE-'].update(data=png_data.getvalue())
    elif event == '-Time-':
        time1 = time.localtime()
        print(time1)

window.close()