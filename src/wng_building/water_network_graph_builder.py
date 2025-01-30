import os

import networkx as nx

from src.data_handling.data_handler import DataHandler
from src.data_handling.dataloader import DataLoader
from src.data_handling.generated_data_handler import GeneratedDataHandler
from src.wng_building.station_river_creator import StationRiverCreator


class WaterNetworkGraphBuilder:
    def __init__(self, dl: DataLoader):
        self.dl = dl

        self.data_handler = DataHandler(dl=self.dl)
        self.station_river_creator = StationRiverCreator(data_handler=self.data_handler)

        self.generated_path = os.path.join(self.dl.data_folder_path, 'generated')

    def run(self):
        self.station_river_creator.run()

        vertices = self.get_vertices()
        self.get_rivers_graph(vertices=vertices)
        self.get_completed_rivers(vertices=vertices)
        self.get_water_network_graph()

    def get_vertices(self) -> list:
        vertices = list(self.station_river_creator.stations.keys())

        GeneratedDataHandler.save_pickle(
            vertices=vertices, edges=[],
            generated_path=self.generated_path,
            folder_name='vertices',
            file_name='vertices'
        )

        return vertices

    def get_rivers_graph(self, vertices: list) -> None:
        for river_name in list(self.station_river_creator.rivers.keys()):
            river = self.station_river_creator.rivers[river_name]
            edges = list(zip(river, river[1:]))

            GeneratedDataHandler.save_pickle(
                vertices=vertices, edges=edges,
                generated_path=self.generated_path,
                folder_name='rivers',
                file_name=river_name
            )

    def get_completed_rivers(self, vertices: list) -> None:
        for river_name in list(self.station_river_creator.completed_rivers.keys()):
            river = self.station_river_creator.completed_rivers[river_name]
            edges = list(zip(river, river[1:]))

            GeneratedDataHandler.save_pickle(
                vertices=vertices, edges=edges,
                generated_path=self.generated_path,
                folder_name='completed_rivers',
                file_name=f'cl_{river_name}'
            )

    def get_water_network_graph(self):
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
