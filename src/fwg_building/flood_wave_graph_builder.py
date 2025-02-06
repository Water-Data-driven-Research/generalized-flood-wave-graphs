import networkx as nx

from src.data_handling.generated_dataloader import GeneratedDataLoader
from src.fwg_building.fwg_data_interface import FWGDataInterface
from src.fwg_building.fwg_preparer_data_interface import FWGPreparerDataInterface


class FloodWaveGraphBuilder:
    def __init__(self, preparer_interface: FWGPreparerDataInterface,
                 do_save_fwg: bool, data_folder_path: str):
        self.preparer_if = preparer_interface
        self.do_save_fwg = do_save_fwg
        self.data_folder_path = data_folder_path

        self.fwg_if = FWGDataInterface()

    def run(self) -> None:
        self.fwg_if.fwg = self.build_flood_wave_graph()

        if self.do_save_fwg:
            self.save_fwg()

    def build_flood_wave_graph(self) -> nx.DiGraph:
        fwg = nx.DiGraph()
        fwg.add_edges_from(self.preparer_if.edges)

        return fwg

    def save_fwg(self) -> None:
        GeneratedDataLoader.save_pickle(
            graph=self.fwg_if.fwg,
            data_folder_path=self.data_folder_path,
            folder_name='flood_wave_graph',
            file_name='fwg'
        )
