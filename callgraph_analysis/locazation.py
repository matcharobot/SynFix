import networkx as nx
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import openai

class Localization:
    """
    Implements the localization phase for identifying suspicious nodes in the CallGraph.
    """

    def __init__(self, graph, openai_api_key):
        """
        Initializes the Localization class.

        :param graph: The CallGraph (a NetworkX DiGraph).
        :param openai_api_key: API key for OpenAI's GPT-3.5.
        """
        self.graph = graph
        self.openai_api_key = openai_api_key
        openai.api_key = self.openai_api_key

    def rank_suspicious_nodes_with_gpt(self, problem_description, top_n=5):
        """
        Uses GPT-3.5 to rank suspicious nodes based on the problem description.

        :param problem_description: A textual description of the problem.
        :param top_n: The number of top suspicious nodes to return.
        :return: A list of top-N suspicious nodes with their relevance scores.
        """
        callgraph_summary = self._generate_callgraph_summary()
        prompt = (
            f"You are tasked with identifying suspicious nodes in a software repository based on the given problem description.\n"
            f"Each node represents a file, class, or function, along with its structural relationships.\n"
            f"The goal is to rank the top {top_n} nodes that are most likely relevant to solving the problem.\n"
            f"\nCallGraph:\n{callgraph_summary}\n"
            f"Problem Statement:\n{problem_description}\n"
            f"\nTask: Provide a ranked list of {top_n} suspicious nodes, along with a brief justification for each."
        )

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an expert software engineer."},
                {"role": "user", "content": prompt}
            ]
        )

        ranked_nodes = self._parse_gpt_response(response["choices"][0]["message"]["content"])
        return ranked_nodes

    def _generate_callgraph_summary(self):
        """
        Generates a textual summary of the CallGraph for GPT-3.5.

        :return: A string summarizing the CallGraph.
        """
        summary = []
        for node, attributes in self.graph.nodes(data=True):
            node_type = attributes.get("type", "unknown")
            summary.append(f"Node: {node} (Type: {node_type})")
            for successor in self.graph.successors(node):
                summary.append(f"  -> {successor}")
        return "\n".join(summary)

    def _parse_gpt_response(self, response_text):
        """
        Parses the GPT-3.5 response to extract ranked nodes and their scores.

        :param response_text: The raw text response from GPT-3.5.
        :return: A list of tuples (node, score).
        """
        ranked_nodes = []
        lines = response_text.split("\n")
        for line in lines:
            if line.strip():
                parts = line.split(":")
                if len(parts) == 2:
                    node = parts[0].strip()
                    try:
                        score = float(parts[1].strip())
                        ranked_nodes.append((node, score))
                    except ValueError:
                        continue
        return ranked_nodes

    def refine_nodes(self, suspicious_nodes, context_depth=1):
        """
        Refines suspicious nodes by including their contextual neighbors in the CallGraph.

        :param suspicious_nodes: A list of suspicious nodes.
        :param context_depth: Depth of neighbors to include in the context.
        :return: A refined list of nodes including contextual neighbors.
        """
        refined_nodes = set(suspicious_nodes)

        for node, _ in suspicious_nodes:
            neighbors = nx.ego_graph(self.graph, node, radius=context_depth).nodes
            refined_nodes.update(neighbors)

        return list(refined_nodes)

if __name__ == "__main__":
    # Example CallGraph
    graph = nx.DiGraph()
    graph.add_node("file1.py", type="file")
    graph.add_node("file1.py:ClassA", type="class")
    graph.add_node("file1.py:ClassA:method1", type="method")
    graph.add_edge("file1.py", "file1.py:ClassA")
    graph.add_edge("file1.py:ClassA", "file1.py:ClassA:method1")

    # API Key (Replace with your own)
    OPENAI_API_KEY = "your_openai_api_key_here"

    localization = Localization(graph, OPENAI_API_KEY)

    # Rank suspicious nodes using GPT-3.5
    problem_description = "Bug in ClassA method"
    top_suspicious = localization.rank_suspicious_nodes_with_gpt(problem_description)
    print("Top Suspicious Nodes:", top_suspicious)

    # Refine nodes with context
    refined = localization.refine_nodes(top_suspicious)
    print("Refined Nodes:", refined)
