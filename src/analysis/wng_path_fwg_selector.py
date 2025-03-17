import copy

import networkx as nx

from src.analysis.fwg_selector_base import FWGSelectorBase
from src.fwg_building.fwg_data_interface import FWGDataInterface
from src.wng_building.wng_data_interface import WNGDataInterface


class WNGPathFWGSelector(FWGSelectorBase):
    """
    Class for selecting a path between two nodes in the WNG, then filtering the FWG
    along this path.
    """
    def __init__(self, data_folder_path: str,
                 fwg_data_if: FWGDataInterface, wng_data_if: WNGDataInterface,
                 do_remove_water_levels: bool = False):
        """
        Constructor.
        :param str data_folder_path: path of the data folder
        :param FWGDataInterface fwg_data_if: an FWGDataInterface instance
        :param WNGDataInterface wng_data_if: a WNGDataInterface instance
        :param bool do_remove_water_levels: True if remove water levels from nodes, hence turning
        three-tuple nodes into two-tuples, False if not
        """
        super().__init__(
            data_folder_path=data_folder_path,
            fwg_data_if=fwg_data_if, wng_data_if=wng_data_if,
            do_remove_water_levels=do_remove_water_levels
        )

    def run(self, temporal_filtering: dict, **kwargs) -> None:
        """
        Run function. Gets the desired path in the WNG and then filters the FWG along this path.
        :param dict temporal_filtering: dictionary containing the start date and end date,
        for example
        {
            'start_date': '2000-01-01',
            'end_date': '2000-02-01'
        }
        **kwargs:
            dict spatial_filtering: Dictionary containing parameters for spatial filtering,
            keys are 'source', 'target' and 'through'. 'through' is a list of additional nodes that
            specify which nodes we would like the path to go through. For example
            {
                'source': '744618',
                'target': '2275',
                'through': []
            }
        """
        spatial_filtering = kwargs.get("spatial_filtering")
        self.get_wng_path(spatial_filtering=spatial_filtering)

        super().run(temporal_filtering=temporal_filtering)

    def get_wng_path(self, spatial_filtering: dict) -> None:
        """
        Gets the only path between spatial_filtering['source'] and spatial_filtering['target']
        that goes through all stations in spatial_filtering['through'].
        :param dict spatial_filtering: spatial filtering dictionary described in the docstring
        of the run function
        """
        all_paths = list(nx.all_simple_paths(
            self.wng,
            source=spatial_filtering['source'],
            target=spatial_filtering['target']
        ))

        for path in all_paths:
            if set(spatial_filtering['through']).issubset(path):
                self.wng_subgraph = copy.deepcopy(self.wng)
                self.wng_subgraph.remove_nodes_from([n for n in self.wng if n not in set(path)])

                return

        raise Exception('There is no path from the source to the target that goes through' 
                        'all given nodes.')
