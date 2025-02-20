import itertools

import networkx as nx


class FloodWaveHandler:
    """
    This is a helper class for FloodWaveExtractor.
    """
    def __init__(self, fwg: nx.DiGraph):
        """
        Constructor.
        :param nx.DiGraph fwg: the Flood Wave Graph
        """
        self.fwg = fwg

    def get_final_pairs(self, comp: list) -> list:
        """
        Searches for end nodes of flood waves in a connected component
        :param list comp: the component
        :return list: list of start and end nodes of flood waves
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

        # condition_one: there is a path from x to y in the WNG
        # condition_two: z(x) > z(y)

        final_pairs = [(x, y) for x, y in cartesian_pairs if condition_one and condition_two]

        return final_pairs
