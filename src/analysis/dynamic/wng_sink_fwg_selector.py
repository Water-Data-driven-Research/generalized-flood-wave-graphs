import copy

import networkx as nx

from src.analysis.dynamic.fwg_selector_base import FWGSelectorBase
from src.fwg_building.fwg_data_interface import FWGDataInterface
from src.wng_building.wng_data_interface import WNGDataInterface


class WNGSinkFWGSelector(FWGSelectorBase):
    """
    Class for getting the largest subgraph of the WNG with a given sink, then filtering
    the FWG with this subgraph.
    """
    def __init__(self, data_folder_path: str,
                 fwg_data_if: FWGDataInterface, wng_data_if: WNGDataInterface,
                 do_remove_water_levels: bool = True):
        """
        Constructor.
        :param str data_folder_path: path of the data folder
        :param FWGDataInterface fwg_data_if: an FWGDataInterface instance
        :param WNGDataInterface wng_data_if: a WNGDataInterface instance
        """
        super().__init__(
            data_folder_path=data_folder_path,
            fwg_data_if=fwg_data_if, wng_data_if=wng_data_if,
            do_remove_water_levels=do_remove_water_levels
        )

    def run(self, temporal_filtering: dict, spatial_filtering: dict) -> None:
        """
        Run function. Gets the desired subgraph in the WNG and then filters the FWG by
        this subgraph.
        :param dict temporal_filtering: dictionary containing the start date and end date,
        for example
        {
            'start_date': '2000-01-01',
            'end_date': '2000-02-01'
        }
        :param dict spatial_filtering: Dictionary containing the reg-number of the desired sink,
        for example
        {
            'sink': '2275'
        }
        """
        self.get_wng_subgraph_with_sink(spatial_filtering=spatial_filtering)

        if self.do_remove_water_levels:
            self.remove_water_levels()

        self.get_fwg_subgraph(temporal_filtering=temporal_filtering)

    def get_wng_subgraph_with_sink(self, spatial_filtering: dict) -> None:
        """
        Gets the largest subgraph of the WNG with the given sink.
        """
        sink = spatial_filtering['sink']
        if sink not in self.wng:
            raise ValueError("Sink node is not in the graph.")

        # Reverse the graph and perform BFS from the given node
        reversed_wng = self.wng.reverse()
        reachable_nodes = set(nx.bfs_tree(reversed_wng, sink).nodes)

        self.wng_subgraph = copy.deepcopy(self.wng)
        self.wng_subgraph.remove_nodes_from([n for n in self.wng if n not in set(reachable_nodes)])
