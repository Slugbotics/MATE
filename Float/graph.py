import pygal


def graph_depth(data, time):
    if len(data) != len(time):
        raise Exception("Depth data is mismatched")
    # Generate the pressure graph
    depth_graph = pygal.Line()
    depth_graph.title = "Depth over time" 
    depth_graph.x_labels = time
    depth_graph.x_title = "UTC time"
    depth_graph.y_title = "Depth (meters)"
    graph_pressure(pressure_data, time)
    depth_graph.add("Depth", data)
    depth_graph.render_to_file("depth_graph.svg")



if __name__ == "__main__":
    with open("float_data.txt") as file:
        data = file.read().split("\n")
    depth_data = [float(x) for x in data[0].split(" ")]
    time = [float(x) for x in data[1].split(" ")]
    graph_depth(depth_data, time)

