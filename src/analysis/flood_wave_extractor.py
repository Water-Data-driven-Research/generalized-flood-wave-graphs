import networkx as nx

from src.analysis.flood_wave_handler import FloodWaveHandler


class FloodWaveExtractor:
    """
    This class is responsible for extracting the flood waves from a given FWG
    """
    def __init__(self, fwg: nx.DiGraph, wng: nx.DiGraph,
                 station_coordinates: dict, equivalence: bool):
        """
        Constructor.
        :param nx.DiGraph fwg: the filtered Flood Wave Graph
        :param nx.DiGraph wng: the filtered Water Network Graph
        :param dict station_coordinates: coordinates of each station in a dictionary
        :param bool equivalence: True if we only consider one element of the equivalence
        classes, False otherwise
        """
        self.fwg = fwg
        self.wng = wng
        self.station_coordinates = station_coordinates
        self.equivalence = equivalence

        self.flood_waves = None

    def run(self) -> None:
        """
        Run function. Gets flood waves.
        """
        if self.equivalence:
            self.get_flood_waves()
        else:
            self.get_flood_waves_without_equivalence()

    def get_flood_waves(self) -> None:
        """
        This function returns the actual flood waves in the FWG with equivalence.
        """
        components = list(nx.weakly_connected_components(self.fwg))

        fw_handler = FloodWaveHandler(
            fwg=self.fwg, wng=self.wng, station_coordinates=self.station_coordinates
        )

        waves = []
        for comp in components:
            possible_pairs = fw_handler.get_possible_pairs(comp=list(comp))

            for start, end in possible_pairs:
                try:
                    wave = nx.shortest_path(self.fwg, start, end)
                    waves.append(list(wave))
                except nx.NetworkXNoPath:
                    continue

        self.flood_waves = waves

    def get_flood_waves_without_equivalence(self) -> None:
        """
        This function returns the actual flood waves in the FWG without equivalence.
        """
        components = list(nx.weakly_connected_components(self.fwg))

        fw_handler = FloodWaveHandler(
            fwg=self.fwg, wng=self.wng, station_coordinates=self.station_coordinates
        )

        waves = []
        for comp in components:
            possible_pairs = fw_handler.get_possible_pairs(comp=list(comp))

            for start, end in possible_pairs:
                try:
                    wave = nx.all_shortest_paths(self.fwg, start, end)
                    waves.append(list(wave))
                except nx.NetworkXNoPath:
                    continue

        self.flood_waves = waves
