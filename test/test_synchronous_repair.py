import networkx as nx
from callgraph_analysis.synchronous_repair import SynchronousRepair

def test_propagate_changes():
    # Arrange
    graph = nx.DiGraph()
    graph.add_node("file1.py", type="file")
    graph.add_node("file1.py:var1", type="variable", parameters="int")
    graph.add_edge("file1.py", "file1.py:var1")
    repair = SynchronousRepair(graph)

    # Act
    graph.nodes["file1.py:var1"]["parameters"] = "float"
    repair.propagate_changes("file1.py:var1")

    # Assert
    assert graph.nodes["file1.py:var1"]["parameters"] == "float"
