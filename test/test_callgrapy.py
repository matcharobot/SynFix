import os
import networkx as nx
from callgraph_analysis.callgraph import CallGraph

def test_callgraph_construction():
    # Arrange
    test_project_path = "test/data/sample_project"
    os.makedirs(test_project_path, exist_ok=True)
    with open(os.path.join(test_project_path, "file1.py"), "w") as f:
        f.write("def function1(): pass")

    # Act
    callgraph = CallGraph(test_project_path)
    graph = callgraph.build()

    # Assert
    assert "file1.py" in graph.nodes
    assert len(graph.nodes) > 0
    assert nx.is_directed(graph)

    # Cleanup
    os.remove(os.path.join(test_project_path, "file1.py"))
    os.rmdir(test_project_path)
