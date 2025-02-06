import networkx as nx

from src.data_handling.generated_dataloader import GeneratedDataLoader
from src.fwg_building.fwg_data_interface import FWGDataInterface
from src.fwg_building.fwg_preparer_data_interface import FWGPreparerDataInterface


class FloodWaveGraphBuilder:
    """
    Class for building the Flood Wave Graph.
    """
    def __init__(self, preparer_interface: FWGPreparerDataInterface,
                 do_save_fwg: bool = False, data_folder_path: str = None):
        """
        Constructor.
        :param FWGPreparerDataInterface preparer_interface: a FWGPreparerDataInterface instance
        :param bool do_save_fwg: whether to save the Flood Wave Graph or not
        :param str data_folder_path: path of the data folder
        """
        self.preparer_if = preparer_interface
        self.do_save_fwg = do_save_fwg
        self.data_folder_path = data_folder_path

        self.fwg_if = FWGDataInterface()

    def run(self) -> None:
        """
        Run function. Builds the Flood Wave Graph and saves it if needed.
        """
        self.fwg_if.fwg = self.build_flood_wave_graph()

        if self.do_save_fwg:
            self.save_fwg()

    def build_flood_wave_graph(self) -> nx.DiGraph:
        """
        Builds the Flood Wave Graph using networkx.
        :return nx.DiGraph: the Flood Wave Graph
        """
        fwg = nx.DiGraph()
        fwg.add_edges_from(self.preparer_if.edges)

        return fwg

    def save_fwg(self) -> None:
        """
        Saves the Flood Wave Graph.
        """
        GeneratedDataLoader.save_pickle(
            graph=self.fwg_if.fwg,
            data_folder_path=self.data_folder_path,
            folder_name='flood_wave_graph',
            file_name='fwg'
        )
