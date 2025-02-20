import copy

import networkx as nx

from src.analysis.position_creator import PositionCreator


class WNGPathFWGPositionCreator:
    """
    Class for creating the positions for plotting the Flood Wave Graph subgraph along a path
    in the Water Network Graph.
    """
    def __init__(self, fwg_subgraph: nx.DiGraph, wng_path: nx.DiGraph):
        """
        Constructor.
        :param nx.DiGraph fwg_subgraph: the FWG subgraph along a path in the WNG
        :param x.DiGraph wng_path: the path in the WNG
        """
        self.fwg_subgraph = fwg_subgraph
        self.reg_numbers = list(wng_path.nodes())

        self.graph_to_plot = nx.DiGraph()
        self.positions = dict()

    def run(self, start_date: str = None, end_date: str = None):
        """
        Run function. Filters the graph between two dates if necessary and creates the positions.
        :param str start_date: start date of the plot
        :param str end_date: end date of the plot
        """
        if start_date is None and end_date is None:
            self.graph_to_plot = self.fwg_subgraph
        elif start_date is not None and end_date is not None:
            self.graph_to_plot = self.cut_graph(start_date=start_date, end_date=end_date)
        else:
            raise Exception('Either give a start date and an end date, or do not give either.')

        self.positions = PositionCreator.create_positions(
            graph=self.graph_to_plot, reg_numbers=self.reg_numbers
        )

    def cut_graph(self, start_date: str, end_date: str) -> nx.DiGraph:
        """
        Function for selecting only nodes between start_date and end_date.
        :param str start_date: start date of the plot
        :param str end_date: end date of the plot
        :return nx.DiGraph: the filtered graph
        """
        nodes_to_plot = []
        for node in self.fwg_subgraph.nodes:
            if start_date <= node[1] <= end_date:
                nodes_to_plot.append(node)

        graph_to_plot = nx.DiGraph(
            copy.deepcopy(
                self.fwg_subgraph.subgraph(nodes_to_plot)
            )
        )
        graph_to_plot.remove_nodes_from(
            list(nx.isolates(graph_to_plot))
        )

        return graph_to_plot
