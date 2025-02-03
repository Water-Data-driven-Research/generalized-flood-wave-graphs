import os

import networkx as nx

from src.data_handling.data_handler import DataHandler
from src.data_handling.dataloader import DataLoader
from src.data_handling.generated_dataloader import GeneratedDataLoader
from src.wng_building.station_river_creator import StationRiverCreator


class WaterNetworkGraphBuilder:
    """
    Class for building the Water Network Graph and saving important data structures
    along the way.
    """
    def __init__(self, dl: DataLoader, do_save_all: bool):
        """
        Constructor.
        :param DataLoader dl: a DataLoader instance
        :param bool do_save_all: whether to save all created data structures or not
        """
        self.dl = dl
        self.do_save_all = do_save_all

        self.data_handler = DataHandler(dl=self.dl)

        self.station_river_creator = StationRiverCreator(
            data_interface=self.data_handler.interface
        )

        self.generated_path = os.path.join(self.dl.ddl.data_folder_path, 'generated')

        self.data = None
        self.vertices = []
        self.river_edges = {}
        self.completed_river_edges = {}
        self.water_network_graph = nx.DiGraph()

    def run(self) -> None:
        """
        Run function. Gets vertices, edges of rivers, edges of completed rivers, the WNG,
        and saves these data structures.
        """
        self.station_river_creator.run()
        self.data = self.station_river_creator.interface

        self.create_vertex_graph()
        self.create_river_graphs()
        self.create_completed_river_graphs()
        self.create_water_network_graph()

        if self.do_save_all:
            self.save_all()

    def create_vertex_graph(self) -> None:
        """
        Gets vertices (all station reg-numbers in a list).
        """
        self.vertices = list(self.data.stations.keys())

    def create_river_graphs(self) -> None:
        """
        Gets the edges of rivers and puts them in a dictionary.
        """
        for river_name in list(self.data.rivers.keys()):
            river = self.data.rivers[river_name]
            edges = list(zip(river, river[1:]))

            self.river_edges[river_name] = edges

    def create_completed_river_graphs(self) -> None:
        """
        Gets the edges of completed rivers and puts them in a dictionary.
        """
        for river_name in list(self.data.completed_rivers.keys()):
            river = self.data.completed_rivers[river_name]
            edges = list(zip(river, river[1:]))

            self.completed_river_edges[river_name] = edges

    def create_water_network_graph(self) -> None:
        """
        Takes the union of the graphs of completed rivers to get the WNG.
        """
        for river_name in list(self.completed_river_edges.keys()):
            completed_river_graph = nx.DiGraph()
            completed_river_graph.add_edges_from(
                self.completed_river_edges[river_name]
            )

            self.water_network_graph = nx.compose(
                self.water_network_graph, completed_river_graph
            )

    def save_all(self) -> None:
        """
        Saves all created data structures: vertices, rivers (individually), completed rivers
        (individually), and the WNG.
        """
        # save vertices
        GeneratedDataLoader.save_pickle(
            vertices=self.vertices, edges=[],
            generated_path=self.generated_path,
            folder_name='vertices',
            file_name='vertices'
        )

        # save rivers and completed rivers individually
        for river_name in list(self.river_edges.keys()):
            # save a river
            GeneratedDataLoader.save_pickle(
                vertices=[], edges=self.river_edges[river_name],
                generated_path=self.generated_path,
                folder_name='rivers',
                file_name=river_name
            )

            # save a completed river
            GeneratedDataLoader.save_pickle(
                vertices=[], edges=self.completed_river_edges[river_name],
                generated_path=self.generated_path,
                folder_name='completed_rivers',
                file_name=f'cl_{river_name}'
            )

        # save the WNG
        GeneratedDataLoader.save_pickle(
            graph=self.water_network_graph,
            generated_path=self.generated_path,
            folder_name='water_network_graph',
            file_name='wng'
        )
