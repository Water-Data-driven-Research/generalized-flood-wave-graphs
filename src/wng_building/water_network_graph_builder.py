import networkx as nx

from src.data_handling.generated_dataloader import GeneratedDataLoader
from src.wng_building.station_river_data_interface import StationRiverDataInterface
from src.wng_building.wng_data_interface import WNGDataInterface


class WaterNetworkGraphBuilder:
    """
    Class for building the Water Network Graph and saving important data structures
    along the way.
    """
    def __init__(self, station_river_if: StationRiverDataInterface,
                 do_save_all: bool, data_folder_path: str):
        """
        Constructor.
        :param StationRiverDataInterface station_river_if: a StationRiverDataInterface instance
        :param bool do_save_all: whether to save all created data structures or not
        :param str data_folder_path: path of the data folder
        """
        self.station_river_if = station_river_if
        self.do_save_all = do_save_all
        self.data_folder_path = data_folder_path

        self.wng_if = WNGDataInterface()

    def run(self) -> None:
        """
        Run function. Gets vertices, edges of rivers, edges of completed rivers, the WNG,
        and saves these data structures.
        """
        completed_river_edges = self.create_completed_river_graphs()
        data = {
            'vertices': self.create_vertex_graph(),
            'river_edges': self.create_river_graphs(),
            'completed_river_edges': completed_river_edges,
            'water_network_graph': self.create_water_network_graph(
                completed_river_edges=completed_river_edges
            )
        }

        self.wng_if = WNGDataInterface(data=data)

        if self.do_save_all:
            self.save_all()

    def create_vertex_graph(self) -> list:
        """
        Gets vertices (all station reg-numbers in a list).
        :return list: vertices of the graph
        """
        return list(self.station_river_if.stations.keys())

    def create_river_graphs(self) -> dict:
        """
        Gets the edges of rivers and puts them in a dictionary.
        """
        river_edges = {}
        for river_name in list(self.station_river_if.rivers.keys()):
            river = self.station_river_if.rivers[river_name]
            edges = list(zip(river, river[1:]))

            river_edges[river_name] = edges

        return river_edges

    def create_completed_river_graphs(self) -> dict:
        """
        Gets the edges of completed rivers and puts them in a dictionary.
        :return dict: the edges of the completed rivers in a dictionary
        """
        completed_river_edges = {}
        for river_name in list(self.station_river_if.completed_rivers.keys()):
            river = self.station_river_if.completed_rivers[river_name]
            edges = list(zip(river, river[1:]))

            completed_river_edges[river_name] = edges

        return completed_river_edges

    @staticmethod
    def create_water_network_graph(completed_river_edges: dict) -> nx.DiGraph:
        """
        Takes the union of the graphs of completed rivers to get the WNG.
        :param dict completed_river_edges: dictionary containing the edges of the
        completed rivers
        :return nx.DiGraph: the WNG
        """
        water_network_graph = nx.DiGraph()
        for river_name in list(completed_river_edges.keys()):
            completed_river_graph = nx.DiGraph()
            completed_river_graph.add_edges_from(
                completed_river_edges[river_name]
            )

            water_network_graph = nx.compose(
                water_network_graph, completed_river_graph
            )

        return water_network_graph

    def save_all(self) -> None:
        """
        Saves all created data structures: vertices, rivers (individually), completed rivers
        (individually), and the WNG.
        """
        # save vertices
        GeneratedDataLoader.save_pickle(
            vertices=self.wng_if.vertices, edges=[],
            data_folder_path=self.data_folder_path,
            folder_name='vertices',
            file_name='vertices'
        )

        # save rivers and completed rivers individually
        for river_name in list(self.wng_if.river_edges.keys()):
            # save a river
            GeneratedDataLoader.save_pickle(
                vertices=[], edges=self.wng_if.river_edges[river_name],
                data_folder_path=self.data_folder_path,
                folder_name='rivers',
                file_name=river_name
            )

            # save a completed river
            GeneratedDataLoader.save_pickle(
                vertices=[], edges=self.wng_if.completed_river_edges[river_name],
                data_folder_path=self.data_folder_path,
                folder_name='completed_rivers',
                file_name=f'cl_{river_name}'
            )

        # save the WNG
        GeneratedDataLoader.save_pickle(
            graph=self.wng_if.water_network_graph,
            data_folder_path=self.data_folder_path,
            folder_name='water_network_graph',
            file_name='wng'
        )
