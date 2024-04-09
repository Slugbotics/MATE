import datetime

import pygal


def graph_depth(data, time):
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

def convert_pressure(pressure):
    # TODO implement pressure to depth conversion
    return pressure


if __name__ == "__main__":
    with open("float_data.txt") as file:
        data = file.read().split("\n")
    time_axis = []
    depth_axis = []
    for time, pressure in data:
        time_axis.append(datetime.fromisoformat(time)) 
        depth_axis.append(convert_pressure(pressure))
    graph_depth(depth_axis, time_axis)

