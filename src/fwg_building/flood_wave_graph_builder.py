import networkx as nx

from src.fwg_building.fwg_data_interface import FWGDataInterface
from src.fwg_building.fwg_preparer_data_interface import FWGPreparerDataInterface


class FloodWaveGraphBuilder:
    def __init__(self, preparer_interface: FWGPreparerDataInterface):
        self.preparer_if = preparer_interface

        self.fwg_if = FWGDataInterface()

    def run(self):
        self.fwg_if.fwg = self.build_flood_wave_graph()

    def build_flood_wave_graph(self) -> nx.DiGraph:
        fwg = nx.DiGraph()
        fwg.add_edges_from(self.preparer_if.edges)

        return fwg
