import os
import pickle

import networkx as nx


class GeneratedDataHandler:

    @staticmethod
    def save_pickle(generated_path: str, folder_name: str,
                    file_name: str,
                    vertices: list = None, edges: list = None,
                    graph: nx.DiGraph = None) -> None:
        os.makedirs(os.path.join(generated_path, folder_name), exist_ok=True)

        if graph is None:
            graph = nx.DiGraph()
            graph.add_nodes_from(vertices)
            graph.add_edges_from(edges)

        with open(os.path.join(generated_path, folder_name, f'{file_name}.pkl'), 'wb') as f:
            pickle.dump(graph, f)

    @staticmethod
    def read_pickle(generated_path: str, folder_name: str,
                    file_name: str) -> nx.DiGraph:
        with open(os.path.join(generated_path, folder_name, f'{file_name}.pkl'), 'rb') as f:
            graph = pickle.load(f)

        return graph
