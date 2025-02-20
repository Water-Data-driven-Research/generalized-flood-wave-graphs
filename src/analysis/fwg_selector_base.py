import copy

import networkx as nx

from src.data_handling.generated_dataloader import GeneratedDataLoader
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
        self.fwg_subgraph = self.get_fwg_subgraph()

    def get_fwg_subgraph(self) -> nx.DiGraph:
        """
        Gets the subgraph by keeping only those (reg_num, date) nodes for which reg_num is
        a node of the WNG and date is between start_date and end_date.
        :return nx.DiGraph: the desired subgraph of the FWG
        """
        nodes_to_keep = []
        for node in self.fwg.nodes:
            condition_one = node[0] in self.wng_subgraph.nodes
            condition_two = (
                    self.temporal_filtering['start_date'] <= node[1] <= self.temporal_filtering['end_date'])

            if condition_one and condition_two:
                nodes_to_keep.append(node)

        subgraph = nx.DiGraph(
            copy.deepcopy(
                self.fwg.subgraph(nodes_to_keep)
            )
        )
        subgraph.remove_nodes_from(
            list(nx.isolates(subgraph))
        )

        return nx.DiGraph(subgraph)
