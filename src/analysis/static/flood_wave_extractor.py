import itertools
from datetime import datetime

import networkx as nx

from src.analysis.static.flood_wave_extractor_interface import FloodWaveExtractorInterface
from src.data_handling.data_interface import DataInterface
from src.data_handling.generated_dataloader import GeneratedDataLoader


class FloodWaveExtractor:
    """
    This class is responsible for extracting the flood waves from a given FWG
    """
    def __init__(self, fwg: nx.DiGraph, wng: nx.DiGraph,
                 data_if: DataInterface, is_equivalence_applied: bool,
                 do_save_flood_waves: bool = False, data_folder_path: str = None):
        """
        Constructor.
        :param nx.DiGraph fwg: the filtered Flood Wave Graph
        :param nx.DiGraph wng: the filtered Water Network Graph
        :param DataInterface data_if: a DataInterface instance
        :param bool is_equivalence_applied: True if we only consider one element of the equivalence
        classes, False otherwise
        :param bool do_save_flood_waves: whether to save extracted flood waves or not
        :param str data_folder_path: path of the data folder
        """
        self.fwg = fwg
        self.wng = wng
        self.station_coordinates = data_if.station_coordinates
        self.is_equivalence_applied = is_equivalence_applied
        self.do_save_flood_waves = do_save_flood_waves
        self.data_folder_path = data_folder_path

        self.extractor_if = FloodWaveExtractorInterface()

    def run(self) -> None:
        """
        Run function. Gets flood waves.
        """
        self.extractor_if.flood_waves = self.get_flood_waves()

        if self.do_save_flood_waves:
            self.save_flood_waves()

    def get_flood_waves(self) -> list:
        """
        This function returns the actual flood waves in the FWG with equivalence.
        :return list: list of extracted flood waves
        """
        components_unsorted = list(nx.weakly_connected_components(self.fwg))
        components = sorted(map(sorted, components_unsorted))

        waves = []
        for comp in components:
            possible_pairs = self.get_possible_pairs(comp=list(comp))

            for start, end in possible_pairs:
                try:
                    if self.is_equivalence_applied:
                        wave = nx.shortest_path(G=self.fwg, source=start, target=end)
                    else:
                        wave = nx.all_shortest_paths(G=self.fwg, source=start, target=end)
                    waves.append(list(wave))
                except nx.NetworkXNoPath:
                    continue

        return waves

    def get_possible_pairs(self, comp: list) -> list:
        """
        Searches for possible starting and end nodes of flood waves in a connected component.
        :param list comp: the component
        :return list: list of tuples of possible start and end nodes
        """
        possible_start_nodes = []
        possible_end_nodes = []
        for node in comp:
            in_deg = self.fwg.in_degree(node)
            out_deg = self.fwg.out_degree(node)

            if in_deg == 0:
                possible_start_nodes.append(node)
            if out_deg == 0:
                possible_end_nodes.append(node)

        start_end_pairs = list(itertools.product(possible_start_nodes, possible_end_nodes))

        possible_pairs = []
        for x, y in start_end_pairs:
            x_reg_number = x[0]
            y_reg_number = y[0]
            x_null_point = self.station_coordinates[x_reg_number]['null_point']
            y_null_point = self.station_coordinates[y_reg_number]['null_point']

            path_exists = nx.has_path(self.wng, x_reg_number, y_reg_number)
            ordering_is_valid = x_null_point > y_null_point

            if path_exists and ordering_is_valid:
                possible_pairs.append((x, y))

        return possible_pairs

    def save_flood_waves(self) -> None:
        """
        Function for saving the flood waves in a dictionary with three keys
        - key 1: 'is_equivalence_applied' -> bool whether we applied equivalence or not
        - key 2: 'stations' -> list of stations in the filtered WNG
        - key 3: 'flood_waves' -> list of all flood waves
        """
        stations = list(self.wng.nodes())
        extracted_flood_waves = {
            'is_equivalence_applied': self.is_equivalence_applied,
            'stations': stations,
            'flood_waves': self.extractor_if.flood_waves
        }

        current_date_and_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        self.extractor_if.timestamp_folder_name = current_date_and_time

        subfolder_names = ['flood_waves', current_date_and_time]

        GeneratedDataLoader.save_json(
            data=extracted_flood_waves,
            data_folder_path=self.data_folder_path,
            subfolder_names=subfolder_names,
            file_name='waves'
        )
