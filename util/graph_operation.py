import networkx as nx

def visualize_graph(graph, filename="graph.png"):
    """
    Visualizes a NetworkX graph and saves it as an image.

    :param graph: The NetworkX graph to visualize.
    :param filename: The name of the file to save the visualization.
    """
    try:
        import matplotlib.pyplot as plt
        pos = nx.spring_layout(graph)
        nx.draw(graph, pos, with_labels=True, node_color='lightblue', edge_color='gray')
        plt.savefig(filename)
        plt.close()
    except ImportError:
        print("matplotlib is required to visualize graphs.")

def get_connected_components(graph):
    """
    Returns the connected components of a graph.

    :param graph: A NetworkX graph.
    :return: A list of connected components.
    """
    return list(nx.connected_components(graph.to_undirected()))
