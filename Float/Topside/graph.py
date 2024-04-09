import datetime

import pygal


def graph_depth(data: list(float), time: list(datetime.datetime)) -> None:
    """Graphs the float data, outputs to 'depth_graph.svg'"""
    if len(data) != len(time):
        raise Exception("Depth data is mismatched")
    # Generate the pressure graph
    depth_graph = pygal.Line()
    depth_graph.title = "Depth over time" 
    depth_graph.x_labels = time
    depth_graph.x_title = "Time"
    depth_graph.y_title = "Depth (meters)"
    graph_pressure(pressure_data, time)
    depth_graph.add("Depth", data)
    depth_graph.render_to_file("depth_graph.svg")

def convert_pressure(pressure: float) -> float:
    """Use the hydrostatic pressure equation to convert pressure to depth"""
    density = 0.992720 # kg / m^3 
    pressure = pressure * 100 # hPa -> Pa
    gravity = 9.81 # m / s^2

    return pressure / (density * gravity) 


def run(date_file: str) -> None:
    """data_file should either be 'float_data_1.txt' or 'float_data_2.txt'"""
    with open(date_file) as file:
        data = file.read().split("\n")
    time_axis = []
    depth_axis = []
    for time, pressure in data:
        time_axis.append(datetime.fromisoformat(time)) 
        depth_axis.append(convert_pressure(pressure))
    graph_depth(depth_axis, time_axis)

