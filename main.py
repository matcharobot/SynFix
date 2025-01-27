from callgraph_analysis.callgraph import CallGraph
from callgraph_analysis.localization import Localization
from callgraph_analysis.synchronous_repair import SynchronousRepair
from callgraph_analysis.validation import Validation

# Example: Initialize and run all components
project_dir = "path_to_project"
callgraph = CallGraph(project_dir)
graph = callgraph.build()

# Localization
localization = Localization(graph, "your_openai_api_key_here")
problem_description = "Example problem statement"
suspicious_nodes = localization.rank_suspicious_nodes_with_gpt(problem_description)

# Synchronous Repair
repair = SynchronousRepair(graph)
for node, _ in suspicious_nodes:
    repair.synchronize_dependencies(node)

# Validation
validator = Validation()
validator.validate_changes()
