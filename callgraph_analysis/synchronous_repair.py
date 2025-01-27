import networkx as nx

class SynchronousRepair:
    """
    Handles the synchronous repair process in the CallGraph.
    Ensures modifications to one node are propagated to its related nodes and dependencies.
    """

    def __init__(self, graph):
        """
        Initializes the SynchronousRepair class.

        :param graph: The CallGraph (a NetworkX DiGraph).
        """
        self.graph = graph

    def propagate_changes(self, modified_node):
        """
        Propagates changes from the modified node to its direct neighbors in the CallGraph.

        :param modified_node: The node in the graph that was modified.
        """
        print(f"Starting propagation from modified node: {modified_node}")
        
        # Retrieve all immediate neighbors of the modified node
        affected_neighbors = list(self.graph.neighbors(modified_node))

        # Apply updates to each neighbor
        for neighbor in affected_neighbors:
            print(f"Propagating changes to neighbor: {neighbor}")
            self._apply_update(neighbor, modified_node)

    def _apply_update(self, target_node, source_node):
        """
        Applies updates to the target node based on the changes in the source node.

        :param target_node: The node to update.
        :param source_node: The node where changes originated.
        """
        print(f"Applying updates from {source_node} to {target_node}")

        source_attributes = self.graph.nodes[source_node]
        target_attributes = self.graph.nodes[target_node]

        # Example: Update parameters or variable types
        if 'parameters' in source_attributes:
            old_parameters = target_attributes.get('parameters', None)
            target_attributes['parameters'] = source_attributes['parameters']
            print(f"Updated parameters for {target_node}: {old_parameters} -> {source_attributes['parameters']}")

        # Example: Update dependent variable types
        if 'type' in source_attributes and source_attributes['type'] == 'variable':
            old_type = target_attributes.get('type', None)
            target_attributes['type'] = source_attributes['type']
            print(f"Updated type for {target_node}: {old_type} -> {source_attributes['type']}")

        # Propagate change logs to track updates
        if 'change_log' in source_attributes:
            if 'change_log' not in target_attributes:
                target_attributes['change_log'] = []
            target_attributes['change_log'].append(f"Updated due to changes in {source_node}")
            print(f"Updated change log for {target_node}: {target_attributes['change_log']}")

    def validate_propagation(self, modified_node):
        """
        Validates that changes have been propagated correctly to all neighbors.

        :param modified_node: The node in the graph that was modified.
        :return: True if all propagations are valid, False otherwise.
        """
        print(f"Validating propagation for modified node: {modified_node}")

        affected_neighbors = list(self.graph.neighbors(modified_node))
        for neighbor in affected_neighbors:
            if not self._is_consistent(modified_node, neighbor):
                print(f"Inconsistency detected between {modified_node} and {neighbor}.")
                return False
        print(f"All propagations from {modified_node} are consistent.")
        return True

    def _is_consistent(self, source_node, target_node):
        """
        Checks if the target node is consistent with the source node.

        :param source_node: The node where changes originated.
        :param target_node: The node to validate.
        :return: True if consistent, False otherwise.
        """
        source_attributes = self.graph.nodes[source_node]
        target_attributes = self.graph.nodes[target_node]

        # Check consistency of parameters
        if 'parameters' in source_attributes and 'parameters' in target_attributes:
            if source_attributes['parameters'] != target_attributes['parameters']:
                print(f"Parameter inconsistency: {source_node} -> {target_node}")
                return False

        # Check consistency of variable types
        if 'type' in source_attributes and 'type' in target_attributes:
            if source_attributes['type'] != target_attributes['type']:
                print(f"Type inconsistency: {source_node} -> {target_node}")
                return False

        return True

    def synchronize_dependencies(self, modified_node):
        """
        Synchronizes all dependencies of a node by recursively propagating changes.

        :param modified_node: The node to synchronize dependencies for.
        """
        print(f"Starting dependency synchronization for node: {modified_node}")
        queue = [modified_node]
        visited = set()

        while queue:
            current_node = queue.pop(0)
            if current_node in visited:
                print(f"Node {current_node} already visited, skipping.")
                continue

            visited.add(current_node)
            print(f"Processing node: {current_node}")

            # Propagate changes to immediate neighbors
            self.propagate_changes(current_node)

            # Add unvisited neighbors to the queue for further synchronization
            neighbors = list(self.graph.neighbors(current_node))
            queue.extend([neighbor for neighbor in neighbors if neighbor not in visited])
        print(f"Dependency synchronization complete for node: {modified_node}")


