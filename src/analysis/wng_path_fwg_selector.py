import networkx as nx

from src.analysis.fwg_selector_base import FWGSelectorBase


class WNGPathFWGSelector(FWGSelectorBase):
    """
    Class for selecting a path between two nodes in the WNG, then filtering the FWG
    along this path.
    """
    def __init__(self, data_folder_path: str,
                 spatial_filtering: dict, temporal_filtering: dict,
                 fwg: nx.DiGraph = None, wng: nx.DiGraph = None):
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
        :param nx.DiGraph fwg: the Flood Wave Graph
        :param nx.DiGraph wng: the Water Network Graph
        """
        super().__init__(
            temporal_filtering=temporal_filtering,
            data_folder_path=data_folder_path,
            fwg=fwg, wng=wng
        )
        self.spatial_filtering = spatial_filtering

    def run(self) -> None:
        """
        Run function. Gets the desired path in the WNG and then filters the FWG along this path.
        """
        self.wng_subgraph = self.get_wng_path()

        super().run()

    def get_wng_path(self) -> nx.DiGraph:
        """
        Gets the only path between spatial_filtering['source'] and spatial_filtering['target']
        that goes through all stations in spatial_filtering['through'].
        :return nx.DiGraph: path of the WNG
        """
        all_paths = list(nx.all_simple_paths(
            self.wng,
            source=self.spatial_filtering['source'],
            target=self.spatial_filtering['target']
        ))

        for path in all_paths:
            if set(self.spatial_filtering['through']).issubset(path):
                path_graph = nx.DiGraph()
                path_graph.add_nodes_from(path)

                return path_graph

        raise Exception('There is no path from the source to the target that goes through' 
                        'all given nodes.')
