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
                 spatial_filtering: dict, temporal_filtering: dict,
                 fwg_data_if: FWGDataInterface, wng_data_if: WNGDataInterface):
        """
        Constructor.
        :param str data_folder_path: path of the data folder
        :param dict spatial_filtering: Dictionary containing parameters for spatial filtering,
        keys are 'source', 'target' and 'through'. 'through' is a list of additional nodes that
        specify which nodes we would like the path to go through. For example
        {
            'source': '744618',
            'target': 2275,
            'through': []
        }
        :param dict temporal_filtering: dictionary containing the start date and end date,
        for example
        {
            'start_date': '2000-01-01',
            'end_date': '2000-02-01'
        }
        :param FWGDataInterface fwg_data_if: an FWGDataInterface instance
        :param WNGDataInterface wng_data_if: a WNGDataInterface instance
        """
        super().__init__(
            temporal_filtering=temporal_filtering,
            data_folder_path=data_folder_path,
            fwg_data_if=fwg_data_if, wng_data_if=wng_data_if
        )
        self.spatial_filtering = spatial_filtering

    def run(self) -> None:
        """
        Run function. Gets the desired path in the WNG and then filters the FWG along this path.
        """
        self.get_wng_path()

        super().run()

    def get_wng_path(self):
        """
        Gets the only path between spatial_filtering['source'] and spatial_filtering['target']
        that goes through all stations in spatial_filtering['through'].
        :return nx.DiGraph: the found path
        """
        all_paths = list(nx.all_simple_paths(
            self.wng,
            source=self.spatial_filtering['source'],
            target=self.spatial_filtering['target']
        ))

        for path in all_paths:
            if set(self.spatial_filtering['through']).issubset(path):
                path_graph = self.wng.subgraph(nodes=path)
                self.wng_subgraph = nx.DiGraph(path_graph)

                return

        raise Exception('There is no path from the source to the target that goes through' 
                        'all given nodes.')
