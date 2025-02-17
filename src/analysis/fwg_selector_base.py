import networkx as nx

from src.data_handling.generated_dataloader import GeneratedDataLoader


class FWGSelectorBase:
    """
    Class for spatial and temporal filtering of the Flood Wave Graph.
    """
    def __init__(self, temporal_filtering: dict,
                 data_folder_path: str,
                 fwg: nx.DiGraph = None, wng: nx.DiGraph = None):
        """
        Constructor.
        :param dict temporal_filtering: {'start_date': start_date, 'end_date': end_date}
        """
        self.fwg = fwg
        self.wng = wng
        self.data_folder_path = data_folder_path
        self.temporal_filtering = temporal_filtering

        if self.fwg is None:
            self.fwg = GeneratedDataLoader.read_pickle(
                data_folder_path=self.data_folder_path,
                folder_name='flood_wave_graph',
                file_name='fwg'
            )

        if self.wng is None:
            self.wng = GeneratedDataLoader.read_pickle(
                data_folder_path=self.data_folder_path,
                folder_name='water_network_graph',
                file_name='wng'
            )

        self.wng_subgraph = nx.DiGraph()
        self.fwg_subgraph = nx.DiGraph()

    def run(self):
        self.fwg_subgraph = self.get_fwg_subgraph()

    def get_fwg_subgraph(self):
        nodes_to_keep = []
        for node in self.fwg.nodes:
            condition_one = node[0] in self.wng_subgraph.nodes
            condition_two = (
                    self.temporal_filtering['start_date'] <= node[1] <= self.temporal_filtering['end_date'])

            if condition_one and condition_two:
                nodes_to_keep.append(node)

        return self.fwg.subgraph(nodes_to_keep).copy()
