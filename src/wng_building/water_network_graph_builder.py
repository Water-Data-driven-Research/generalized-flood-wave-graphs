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
    def __init__(self, dl: DataLoader):
        """
        Constructor.
        :param DataLoader dl: a DataLoader instance
        """
        self.dl = dl

        self.data_handler = DataHandler(dl=self.dl)

        self.station_river_creator = StationRiverCreator(
            data_interface=self.data_handler.interface
        )

        self.generated_path = os.path.join(self.dl.ddl.data_folder_path, 'generated')

        self.data = None

    def run(self) -> None:
        """
        Run function. Gets and saves vertices, saves rivers, completed rivers and
        the Water Network Graph.
        """
        self.station_river_creator.run()
        self.data = self.station_river_creator.interface

        self.create_vertex_graph()
        self.create_river_graphs()
        self.create_completed_river_graphs()
        self.create_water_network_graph()

    def create_vertex_graph(self) -> None:
        """
        Gets and saves vertices to data/generated/vertices as a graph of isolated nodes.
        """
        vertices = list(self.data.stations.keys())

        GeneratedDataLoader.save_pickle(
            vertices=vertices, edges=[],
            generated_path=self.generated_path,
            folder_name='vertices',
            file_name='vertices'
        )

    def create_river_graphs(self) -> None:
        """
        Gets the rivers and saves them to data/generated/rivers as different graphs of
        directed paths.
        """
        for river_name in list(self.data.rivers.keys()):
            river = self.data.rivers[river_name]
            edges = list(zip(river, river[1:]))

            GeneratedDataLoader.save_pickle(
                vertices=[], edges=edges,
                generated_path=self.generated_path,
                folder_name='rivers',
                file_name=river_name
            )

    def create_completed_river_graphs(self) -> None:
        """
        Gets the completed rivers and saves them to data/generated/completed_rivers as different
        graphs of directed paths.
        """
        for river_name in list(self.data.completed_rivers.keys()):
            river = self.data.completed_rivers[river_name]
            edges = list(zip(river, river[1:]))

            GeneratedDataLoader.save_pickle(
                vertices=[], edges=edges,
                generated_path=self.generated_path,
                folder_name='completed_rivers',
                file_name=f'cl_{river_name}'
            )

    def create_water_network_graph(self) -> None:
        """
        Reads the completed rivers and takes their union -> this is the Water Network Graph (WNG)
        Saves the WNG to data/generated/water_network_graph
        """
        water_network_graph = nx.DiGraph()
        for river_name in list(self.data.completed_rivers.keys()):
            completed_river = GeneratedDataLoader.read_pickle(
                generated_path=self.generated_path,
                folder_name='completed_rivers',
                file_name=f'cl_{river_name}'
            )

            water_network_graph = nx.compose(water_network_graph, completed_river)

        GeneratedDataLoader.save_pickle(
            graph=water_network_graph,
            generated_path=self.generated_path,
            folder_name='water_network_graph',
            file_name='wng'
        )
