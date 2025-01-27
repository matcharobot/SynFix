import networkx as nx
from callgraph_analysis.localization import Localization

def test_localization():
    # Arrange
    graph = nx.DiGraph()
    graph.add_node("file1.py", type="file")
    graph.add_node("file1.py:func1", type="function", name="func1")
    graph.add_edge("file1.py", "file1.py:func1")

    localization = Localization(graph, "your_openai_api_key_here")

    # Act
    suspicious_nodes = localization.rank_suspicious_nodes_with_gpt("Bug in func1")

    # Assert
    assert len(suspicious_nodes) > 0
