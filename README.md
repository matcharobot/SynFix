
# SynFix: Synchronous Repair for Codebase via CallGraph

## Overview
SynFix is an automated program repair framework that leverages a CallGraph-based approach to identify, localize, and repair bugs in large codebases. The tool integrates machine learning, static analysis, and systematic validation to ensure effective and consistent code repair.

### Key Features
- **CallGraph Construction**: Builds a hierarchical CallGraph to represent relationships between files, classes, functions, and variables.
- **Suspicious Node Localization**: Identifies and ranks the most likely code regions responsible for bugs using GPT-3.5 and embedding-based retrieval.
- **Synchronous Repair**: Propagates changes across dependent nodes in the CallGraph to maintain consistency.
- **Validation**: Runs regression tests to ensure that repairs do not introduce new bugs.
- **Utility Modules**: Reusable utilities for file operations, logging, and API interactions.

---

## Project Structure
```
SynFix/
├── callgraph_analysis/
│   ├── callgraph.py          # Handles CallGraph construction
│   ├── localization.py       # Identifies and ranks suspicious nodes
│   ├── synchronous_repair.py # Propagates changes and validates consistency
│   ├── validation.py         # Executes regression tests
├── util/
│   ├── api_requests.py       # Handles OpenAI GPT queries
│   ├── file_operations.py    # Provides file and directory utilities
│   ├── graph_operations.py   # Helper functions for graph manipulations
│   ├── logger.py             # Logging utilities
├── test/
│   ├── test_callgraph.py     # Unit tests for CallGraph
│   ├── test_localization.py  # Unit tests for Localization
│   ├── test_synchronous_repair.py # Unit tests for Synchronous Repair
│   ├── test_validation.py    # Unit tests for Validation
│   ├── integration_test.py   # End-to-end testing
├── main.py                   # Main script to execute the pipeline
└── README.md                 # Project documentation
```

---

## Installation

### Prerequisites
- Python 3.8 or higher
- Required libraries:
  ```bash
  pip install networkx openai pytest
  ```

### Clone the Repository
```bash
git clone https://github.com/your-repo/SynFix.git
cd SynFix
```

---

## Usage

### 1. Build the CallGraph
Construct a CallGraph for the target codebase:
```python
from callgraph_analysis.callgraph import CallGraph

project_dir = "path_to_project"
callgraph = CallGraph(project_dir)
graph = callgraph.build()
```

### 2. Identify Suspicious Nodes
Use GPT-3.5 to rank suspicious nodes:
```python
from callgraph_analysis.localization import Localization

localization = Localization(graph, "your_openai_api_key_here")
problem_description = "Bug in processing function"
suspicious_nodes = localization.rank_suspicious_nodes_with_gpt(problem_description)
print(suspicious_nodes)
```

### 3. Perform Synchronous Repair
Propagate changes across the CallGraph:
```python
from callgraph_analysis.synchronous_repair import SynchronousRepair

repair = SynchronousRepair(graph)
for node, _ in suspicious_nodes:
    repair.synchronize_dependencies(node)
```

### 4. Validate Changes
Run regression tests to validate repairs:
```python
from callgraph_analysis.validation import Validation

validator = Validation()
validator.validate_changes()
```

### 5. Integration Test
Run the entire pipeline using `main.py`:
```bash
python main.py
```

---

## Testing

### Run All Tests
Use `pytest` to execute all tests:
```bash
pytest test/
```

### Test Coverage
- **Unit Tests**: Validate individual modules.
- **Integration Tests**: Test the entire pipeline.

---

## Contributing

We welcome contributions! Follow these steps:
1. Fork the repository.
2. Create a feature branch.
3. Commit your changes.
4. Submit a pull request.

---

## License
This project is licensed under the MIT License. See `LICENSE` for more details.

---

## Acknowledgments
- **OpenAI** for GPT-3.5 integration.
- **NetworkX** for graph operations.

