import copy

import networkx as nx

from src.fwg_building.fwg_data_interface import FWGDataInterface
from src.wng_building.wng_data_interface import WNGDataInterface


class FWGSelectorBase:
    """
    Class for spatial and temporal filtering of the Flood Wave Graph.
    """
    def __init__(self, temporal_filtering: dict,
                 data_folder_path: str,
                 fwg_data_if: FWGDataInterface, wng_data_if: WNGDataInterface):
        """
        Constructor.
        :param dict temporal_filtering: {'start_date': start_date, 'end_date': end_date}
        :param str data_folder_path: path of the data folder
        :param FWGDataInterface fwg_data_if: an FWGDataInterface instance
        :param WNGDataInterface wng_data_if: a WNGDataInterface instance
        """
        self.fwg = fwg_data_if.flood_wave_graph
        self.wng = wng_data_if.water_network_graph
        self.data_folder_path = data_folder_path
        self.temporal_filtering = temporal_filtering

        self.wng_subgraph = nx.DiGraph()
        self.fwg_subgraph = nx.DiGraph()

    def run(self) -> None:
        """
        Run function. Gets the desired subgraph of the FWG.
        """
        self.get_fwg_subgraph()

    def get_fwg_subgraph(self):
        """
        Gets the subgraph by keeping only those (reg_num, date) nodes for which reg_num is
        a node of the WNG and date is between start_date and end_date.
        """
        nodes_to_keep = []
        for node in self.fwg.nodes:
            is_node_in_subgraph = node[0] in self.wng_subgraph.nodes
            is_date_between_bounds = (
                    self.temporal_filtering['start_date'] <= node[1] <= self.temporal_filtering['end_date'])

            if is_node_in_subgraph and is_date_between_bounds:
                nodes_to_keep.append(node)

        self.fwg_subgraph = copy.deepcopy(self.fwg)
        self.fwg_subgraph.remove_nodes_from(
            [n for n in self.fwg if n not in nodes_to_keep]
        )
        self.fwg_subgraph.remove_nodes_from(
            list(nx.isolates(self.fwg_subgraph))
        )
