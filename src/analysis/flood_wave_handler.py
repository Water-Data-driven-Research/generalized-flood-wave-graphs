import itertools

import networkx as nx


class FloodWaveHandler:
    """
    This is a helper class for FloodWaveExtractor.
    """
    def __init__(self, fwg: nx.DiGraph, wng: nx.DiGraph,
                 station_coordinates: dict):
        """
        Constructor.
        :param nx.DiGraph fwg: the filtered Flood Wave Graph
        :param nx.DiGraph wng: the filtered Water Network Graph
        :param dict station_coordinates: coordinates of each station in a dictionary
        """
        self.fwg = fwg
        self.wng = wng
        self.station_coordinates = station_coordinates

    def get_final_pairs(self, comp: list) -> list:
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

        cartesian_pairs = list(itertools.product(possible_start_nodes, possible_end_nodes))

        final_pairs = []
        for x, y in cartesian_pairs:
            x_reg_number = x[0]
            y_reg_number = y[0]
            x_null_point = self.station_coordinates[x_reg_number]['null_point']
            y_null_point = self.station_coordinates[y_reg_number]['null_point']

            path_exists = nx.has_path(self.wng, x_reg_number, y_reg_number)
            ordering_is_valid = x_null_point > y_null_point

            if path_exists and ordering_is_valid:
                final_pairs.append((x, y))

        return final_pairs
