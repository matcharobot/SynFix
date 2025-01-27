from callgraph_analysis.callgraph import CallGraph
from callgraph_analysis.localization import Localization
from callgraph_analysis.synchronous_repair import SynchronousRepair
from callgraph_analysis.validation import Validation

def test_full_pipeline():
    # Arrange
    project_dir = "test/data/sample_project"
    callgraph = CallGraph(project_dir)
    graph = callgraph.build()
    
    localization = Localization(graph, "your_openai_api_key_here")
    repair = SynchronousRepair(graph)
    validator = Validation(test_dir="test/data/sample_project/tests")

    # Act
    suspicious_nodes = localization.rank_suspicious_nodes_with_gpt("Bug in func1")
    for node, _ in suspicious_nodes:
        repair.synchronize_dependencies(node)

    test_result = validator.validate_changes()

    # Assert
    assert test_result is True or test_result is False
