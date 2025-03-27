from datetime import datetime

import networkx as nx


class PositionCreator:
    """
    Class for creating positions of nodes for plotting.
    """
    @staticmethod
    def create_positions(graph: nx.DiGraph, reg_numbers: list) -> dict:
        """
        Creates positions. x coordinates are dates with a frequency of 1 day, y coordinates
        are reg-numbers in order
        :param nx.DiGraph graph: graph to plot
        :param list reg_numbers: the reg-numbers of the stations
        :return dict: the positions in a dictionary, keys are the nodes and values are
        the positions
        """
        min_date_temp = min([node[1] for node in graph.nodes()])
        min_date = datetime.strptime(min_date_temp, '%Y-%m-%d')

        positions = dict()
        for node in graph.nodes():
            x_coord = (datetime.strptime(node[1], '%Y-%m-%d') - min_date).days - 1
            y_coord = len(reg_numbers) - reg_numbers.index(node[0])
            positions[node] = (x_coord, y_coord)

        return positions
