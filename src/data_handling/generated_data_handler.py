import os
import pickle

import networkx as nx


class GeneratedDataHandler:

    @staticmethod
    def save_pickle(vertices: list, edges: list,
                    data_folder_path: str, file_name: str):
        os.makedirs(os.path.join(data_folder_path, 'generated'), exist_ok=True)

        graph = nx.DiGraph()

        graph.add_nodes_from(vertices)
        graph.add_edges_from(edges)

        with open(os.path.join(data_folder_path, 'generated', f'{file_name}.pkl'), 'wb') as f:
            pickle.dump(graph, f)

    @staticmethod
    def read_pickle(data_folder_path: str, file_name: str) -> nx.DiGraph:
        with open(os.path.join(data_folder_path, 'generated', f'{file_name}.pkl'), 'rb') as f:
            graph = pickle.load(f)

        return graph
