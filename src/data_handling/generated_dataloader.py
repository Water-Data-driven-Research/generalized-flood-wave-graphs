import json
import os
import pickle

import networkx as nx


class GeneratedDataLoader:
    """
    Class for writing and reading pickle files.
    """

    @staticmethod
    def save_pickle(data_folder_path: str, folder_name: str,
                    file_name: str,
                    vertices: list = None, edges: list = None,
                    graph: nx.DiGraph = None) -> None:
        """
        Method for saving a graph into a pickle file. We can pass a graph or build it
        inside this method from the given vertices and edges.
        :param str data_folder_path: path of the data folder
        :param str folder_name: name of the folder inside the generated folder
        :param str file_name: name of the file
        :param list vertices: list of vertices
        :param list edges: list of nodes
        :param nx.DiGraph graph: networkx directed graph
        """
        os.makedirs(os.path.join(data_folder_path, 'generated', folder_name), exist_ok=True)

        if graph is None:
            graph = nx.DiGraph()
            graph.add_nodes_from(vertices)
            graph.add_edges_from(edges)

        with open(os.path.join(
                data_folder_path, 'generated', folder_name, f'{file_name}.pkl'
        ), 'wb') as f:
            pickle.dump(graph, f)

    @staticmethod
    def read_pickle(data_folder_path: str, folder_name: str,
                    file_name: str) -> nx.DiGraph:
        """
        Method for reading pickle files and returning the resulted directed graph
        :param str data_folder_path: path of the data folder
        :param str folder_name: name of the folder inside the generated folder
        :param str file_name: name of the file
        :return nx.DiGraph: networkx directed graph
        """
        with open(os.path.join(
                data_folder_path, 'generated', folder_name, f'{file_name}.pkl'
        ), 'rb') as f:
            graph = pickle.load(f)

        return graph

    @staticmethod
    def save_json(data: dict, data_folder_path: str,
                  subfolder_names: list, file_name: str) -> None:
        """
        Function for saving dictionaries into json files.
        :param dict data: dictionary we wish to save
        :param str data_folder_path: path of the data folder
        :param list subfolder_names: there nested folder will be created and the file will be
        saved in the rightmost folder
        :param str file_name: name of the json file
        """
        folder_names_chain = ['generated'] + subfolder_names
        os.makedirs(os.path.join(data_folder_path, *folder_names_chain), exist_ok=True)

        with open(os.path.join(data_folder_path, *folder_names_chain, f"{file_name}.json"), "w") as f:
            json.dump(data, f)

    @staticmethod
    def read_json(data_folder_path: str, subfolder_names: list, file_name: str) -> dict:
        """
        Function for loading json files into dictionaries.
        :param str data_folder_path: path of the data folder
        :param list subfolder_names: there nested folder will be created and the file will be
        saved in the rightmost folder
        :param str file_name: name of the json file
        :return dict: the loaded dictionary
        """
        folder_names_chain = ['generated'] + subfolder_names
        with open(os.path.join(data_folder_path, *folder_names_chain, f"{file_name}.json"), "r") as f:
            loaded_data = json.load(f)

        return loaded_data
