import networkx as nx

from src.analysis.fwg_selector_base import FWGSelectorBase


class WNGPathFWGSelector(FWGSelectorBase):
    def __init__(self, data_folder_path: str,
                 spatial_filtering: dict, temporal_filtering: dict,
                 fwg: nx.DiGraph = None, wng: nx.DiGraph = None):
        super().__init__(
            temporal_filtering=temporal_filtering,
            data_folder_path=data_folder_path,
            fwg=fwg, wng=wng
        )
        self.spatial_filtering = spatial_filtering

    def run(self):
        self.wng_subgraph = self.get_wng_path()

        super().run()

    def get_wng_path(self) -> nx.DiGraph:
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
