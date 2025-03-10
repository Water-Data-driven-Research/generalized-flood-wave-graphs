import networkx as nx

from src.data_handling.data_interface import DataInterface


class WNGSinkFWGPlotPreparer:
    """
    Class for preparing the FWG subgraph with sink(s) for interactive plotting.
    """
    def __init__(self, data_if: DataInterface,
                 fwg_subgraph: nx.DiGraph, wng_subgraph: nx.DiGraph):
        """
        Constructor.
        :param DataInterface data_if: a DataInterface instance
        :param nx.DiGraph fwg_subgraph: the FWG subgraph above the WNG subgraph with a sink
        :param nx.DiGraph wng_subgraph: the WNG subgraph with a sink
        """
        self.station_coordinates = data_if.station_coordinates
        self.fwg_subgraph = fwg_subgraph
        self.wng_subgraph = wng_subgraph

        self.node_positions = {}
        self.dates_dict = {node: [] for node in self.wng_subgraph.nodes}

    def run(self) -> None:
        """
        Gets positions and creates a dictionary containing the dates for each node.
        """
        self.create_positions_and_get_dates_dict()

    def create_positions_and_get_dates_dict(self) -> None:
        """
        Stores the coordinates of each node in a dictionary. Moreover, creates a dictionary
        containing the dates for each node.
        """
        for node in self.fwg_subgraph.nodes:
            # the definition of EOV coordinates suggests that x should be EOVy and
            # y should be EOVx
            base_x = self.station_coordinates[node[0]]['EOVy']
            base_y = self.station_coordinates[node[0]]['EOVx']
            self.node_positions[node] = (base_x, base_y)

            self.dates_dict[node[0]].append(node[1])
