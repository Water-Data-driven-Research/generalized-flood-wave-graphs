import os

import networkx as nx

from src.data_handling.data_handler import DataHandler
from src.data_handling.dataloader import DataLoader
from src.data_handling.generated_data_handler import GeneratedDataHandler
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
        self.station_river_creator = StationRiverCreator(data_handler=self.data_handler)

        self.generated_path = os.path.join(self.dl.data_folder_path, 'generated')

    def run(self) -> None:
        """
        Run function. Gets and saves vertices, saves rivers, completed rivers and
        the Water Network Graph.
        """
        self.station_river_creator.run()

        self.save_vertices()
        self.save_rivers()
        self.save_completed_rivers()
        self.save_water_network_graph()

    def save_vertices(self) -> None:
        """
        Gets and saves vertices to data/generated/vertices as a graph of isolated nodes.
        """
        vertices = list(self.station_river_creator.stations.keys())

        GeneratedDataHandler.save_pickle(
            vertices=vertices, edges=[],
            generated_path=self.generated_path,
            folder_name='vertices',
            file_name='vertices'
        )

    def save_rivers(self) -> None:
        """
        Gets the rivers and saves them to data/generated/rivers as different graphs of
        directed paths.
        """
        for river_name in list(self.station_river_creator.rivers.keys()):
            river = self.station_river_creator.rivers[river_name]
            edges = list(zip(river, river[1:]))

            GeneratedDataHandler.save_pickle(
                vertices=[], edges=edges,
                generated_path=self.generated_path,
                folder_name='rivers',
                file_name=river_name
            )

    def save_completed_rivers(self) -> None:
        """
        Gets the completed rivers and saves them to data/generated/completed_rivers as different
        graphs of directed paths.
        """
        for river_name in list(self.station_river_creator.completed_rivers.keys()):
            river = self.station_river_creator.completed_rivers[river_name]
            edges = list(zip(river, river[1:]))

            GeneratedDataHandler.save_pickle(
                vertices=[], edges=edges,
                generated_path=self.generated_path,
                folder_name='completed_rivers',
                file_name=f'cl_{river_name}'
            )

    def save_water_network_graph(self) -> None:
        """
        Reads the completed rivers and takes their union -> this is the Water Network Graph (WNG)
        Saves the WNG to data/generated/water_network_graph
        """
        water_network_graph = nx.DiGraph()
        for river_name in list(self.station_river_creator.completed_rivers.keys()):
            completed_river = GeneratedDataHandler.read_pickle(
                generated_path=self.generated_path,
                folder_name='completed_rivers',
                file_name=f'cl_{river_name}'
            )

            water_network_graph = nx.compose(water_network_graph, completed_river)

        GeneratedDataHandler.save_pickle(
            graph=water_network_graph,
            generated_path=self.generated_path,
            folder_name='water_network_graph',
            file_name=f'wng'
        )
