import itertools

import networkx as nx


class FloodWaveExtractor:
    """
    This class is responsible for extracting the flood waves from a given FWG
    """
    def __init__(self, fwg: nx.DiGraph, wng: nx.DiGraph,
                 station_coordinates: dict, is_equivalence_applied: bool):
        """
        Constructor.
        :param nx.DiGraph fwg: the filtered Flood Wave Graph
        :param nx.DiGraph wng: the filtered Water Network Graph
        :param dict station_coordinates: coordinates of each station in a dictionary
        :param bool is_equivalence_applied: True if we only consider one element of the equivalence
        classes, False otherwise
        """
        self.fwg = fwg
        self.wng = wng
        self.station_coordinates = station_coordinates
        self.is_equivalence_applied = is_equivalence_applied

        self.flood_waves = []

    def run(self) -> None:
        """
        Run function. Gets flood waves.
        """
        self.get_flood_waves()

    def get_flood_waves(self) -> None:
        """
        This function returns the actual flood waves in the FWG with equivalence.
        """
        components = list(nx.weakly_connected_components(self.fwg))

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

        self.flood_waves = waves

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
