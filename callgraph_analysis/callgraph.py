import os
import ast
import networkx as nx

class ClassFunctionVisitor(ast.NodeVisitor):
    def __init__(self):
        self.defs = {}

    def visit_ClassDef(self, node):
        self.defs[node.name] = [f.name for f in node.body if isinstance(f, ast.FunctionDef)]
        self.generic_visit(node)

    def visit_FunctionDef(self, node):
        if node.name not in self.defs:
            self.defs[node.name] = []

class VariableVisitor(ast.NodeVisitor):
    def __init__(self):
        self.assignments = {}  # Record variable definitions
        self.usage = {}  # Record variable usages

    def visit_Assign(self, node):
        for target in node.targets:
            if isinstance(target, ast.Name):
                var_name = target.id
                if var_name not in self.assignments:
                    self.assignments[var_name] = []
                self.assignments[var_name].append((node.lineno, node.col_offset))
        self.generic_visit(node)

    def visit_Name(self, node):
        if isinstance(node.ctx, ast.Load):
            var_name = node.id
            if var_name not in self.usage:
                self.usage[var_name] = []
            self.usage[var_name].append((node.lineno, node.col_offset))
        self.generic_visit(node)

def extract_defs(filename):
    try:
        with open(filename, "r") as source:
            tree = ast.parse(source.read())
            class_visitor = ClassFunctionVisitor()
            var_visitor = VariableVisitor()
            class_visitor.visit(tree)
            var_visitor.visit(tree)
        return class_visitor.defs, var_visitor.assignments, var_visitor.usage
    except IndentationError as e:
        print(f"IndentationError in file {filename}: {e}")
        return {}, {}, {}

def create_graph(root_dir):
    G = nx.DiGraph()
    var_definitions = {}  # Track where each variable is defined

    for dirpath, dirnames, filenames in os.walk(root_dir):
        parent_name = os.path.basename(dirpath)
        if parent_name == '':
            parent_name = root_dir  # Special handling for root directory
        for filename in filenames:
            if filename.endswith('.py'):
                file_node = os.path.join(parent_name, filename)
                G.add_edge(parent_name, file_node)
                full_path = os.path.join(dirpath, filename)
                defs, assignments, usage = extract_defs(full_path)
                for def_name, subdefs in defs.items():
                    class_node = f"{file_node}:{def_name}"
                    G.add_edge(file_node, class_node)
                    for subdef in subdefs:
                        method_node = f"{class_node}:{subdef}"
                        G.add_edge(class_node, method_node)
                for var_name, locations in assignments.items():
                    var_def_node = f"{file_node}:{var_name}_def"
                    var_definitions[var_name] = file_node
                    G.add_edge(file_node, var_def_node)
                for var_name, locations in usage.items():
                    var_usage_node = f"{file_node}:{var_name}_usage"
                    for loc in locations:
                        if var_name in var_definitions:
                            def_file = var_definitions[var_name]
                            var_def_node = f"{def_file}:{var_name}_def"
                            G.add_edge(var_def_node, var_usage_node)
                        G.add_edge(file_node, var_usage_node)

        for dirname in dirnames:
            next_dirpath = os.path.join(dirpath, dirname)
            next_dirname = os.path.basename(next_dirpath)
            if any(fname.endswith('.py') for fname in os.listdir(next_dirpath)):
                G.add_edge(parent_name, next_dirname)

    return G

def update_graph(G, file_path, fix_code):
    """
    Updates the graph to reflect code changes in a specific file.

    :param G: The CallGraph to update.
    :param file_path: The path to the modified file.
    :param fix_code: The new code that replaced or modified the file's content.
    """
    # Analyze the modified file's content
    defs, assignments, usage = extract_defs(file_path)

    # Update or add nodes for functions and classes
    for def_name, subdefs in defs.items():
        class_node = f"{file_path}:{def_name}"
        if not G.has_node(class_node):
            G.add_node(class_node, type='class')
            G.add_edge(file_path, class_node)
        for subdef in subdefs:
            method_node = f"{class_node}:{subdef}"
            if not G.has_node(method_node):
                G.add_node(method_node, type='method')
                G.add_edge(class_node, method_node)

    # Update or add nodes for variable definitions
    var_definitions = {}
    for var_name, locations in assignments.items():
        var_def_node = f"{file_path}:{var_name}_def"
        if not G.has_node(var_def_node):
            G.add_node(var_def_node, type='variable')
            G.add_edge(file_path, var_def_node)
        var_definitions[var_name] = var_def_node

    # Update or add edges for variable usage
    for var_name, locations in usage.items():
        for loc in locations:
            var_usage_node = f"{file_path}:{var_name}_usage:{loc[0]}:{loc[1]}"
            if not G.has_node(var_usage_node):
                G.add_node(var_usage_node, type='variable_usage')
            if var_name in var_definitions:
                G.add_edge(var_definitions[var_name], var_usage_node)
            G.add_edge(file_path, var_usage_node)

    # Update neighboring relationships
    affected_nodes = list(nx.neighbors(G, file_path))
    for node in affected_nodes:
        if G.nodes[node].get('type') == 'class':
            # Propagate changes to methods if the class is affected
            for successor in G.successors(node):
                if G.nodes[successor].get('type') == 'method':
                    print(f"Class {node} affected method {successor}, consider revalidating.")
        elif G.nodes[node].get('type') == 'variable':
            # Propagate changes to variable usages if the variable is affected
            for successor in G.successors(node):
                if G.nodes[successor].get('type') == 'variable_usage':
                    print(f"Variable {node} affected usage {successor}, consider revalidating.")

