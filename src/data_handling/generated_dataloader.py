import os
import pickle

import networkx as nx


class GeneratedDataLoader:
    """
    Class for writing and reading pickle files.
    """

    @staticmethod
    def save_pickle(generated_path: str, folder_name: str,
                    file_name: str,
                    vertices: list = None, edges: list = None,
                    graph: nx.DiGraph = None) -> None:
        """
        Method for saving a graph into a pickle file. We can pass a graph or build it
        inside this method from the given vertices and edges.
        :param str generated_path: path of the generated folder
        :param str folder_name: name of the folder inside the generated folder
        :param str file_name: name of the file
        :param list vertices: list of vertices
        :param list edges: list of nodes
        :param nx.DiGraph graph: networkx directed graph
        """
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
        """
        Method for reading pickle files and returning the resulted directed graph
        :param str generated_path: path of the generated folder
        :param str folder_name: name of the folder inside the generated folder
        :param str file_name: name of the file
        :return nx.DiGraph: networkx directed graph
        """
        with open(os.path.join(generated_path, folder_name, f'{file_name}.pkl'), 'rb') as f:
            graph = pickle.load(f)

        return graph
