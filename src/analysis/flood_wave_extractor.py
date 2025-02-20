import networkx as nx

from src.analysis.flood_wave_handler import FloodWaveHandler


class FloodWaveExtractor:
    """
    This class is responsible for extracting the flood waves from a given FWG
    """
    def __init__(self, fwg: nx.DiGraph):
        """
        Constructor.
        :param nx.DiGraph fwg: the graph
        """
        self.fwg = fwg
        self.flood_waves = None

    def get_flood_waves(self):
        """
        This function returns the actual flood waves in the graph
        :return list: list of lists of the flood wave nodes
        """
        components = list(nx.weakly_connected_components(self.fwg))

        fw_handler = FloodWaveHandler(fwg=self.fwg)

        waves = []
        for comp in components:
            final_pairs = fw_handler.get_final_pairs(comp=list(comp))

            for start, end in final_pairs:
                try:
                    wave = nx.shortest_path(self.fwg, start, end)
                    waves.append((wave[0], wave[-1]))
                except nx.NetworkXNoPath:
                    continue

        self.flood_waves = waves

    def get_flood_waves_without_equivalence(self):
        """
        This function returns all the 'elements' of the theoretical flood wave equivalence classes (so for given
        start and end nodes it takes all paths between them)
        :return list: paths
        """
        components = list(nx.weakly_connected_components(self.fwg))

        fw_handler = FloodWaveHandler(fwg=self.fwg)

        waves = []
        for comp in components:
            final_pairs = fw_handler.get_final_pairs(comp=list(comp))

            for start, end in final_pairs:
                try:
                    wave = nx.all_shortest_paths(self.fwg, start, end)
                    waves.append(list(wave))
                except nx.NetworkXNoPath:
                    continue

        self.flood_waves = waves

    @staticmethod
    def get_flood_waves_from_start_to_end(waves: list,
                                          start_station: str,
                                          end_station: str,
                                          equivalence: bool) -> list:
        """
        Selects only those flood waves that impacted both the start_station and end_station
        :param list waves: list of all the flood waves
        :param str start_station: the start station
        :param str end_station: the end station
        :param bool equivalence: True if we only consider one element of the equivalence classes, False otherwise
        :return list: full flood waves
        """
        if equivalence:
            final_waves = []
            for wave in waves:
                if start_station == wave[0][0] and end_station == wave[1][0]:
                    final_waves.append(wave)

        else:
            final_waves = []
            for paths in waves:
                if start_station == paths[0][0][0] and end_station == paths[0][-1][0]:
                    final_waves.append(paths)

        return final_waves
