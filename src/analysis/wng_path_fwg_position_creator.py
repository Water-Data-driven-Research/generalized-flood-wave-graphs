import copy
from datetime import datetime

import networkx as nx


class WNGPathFWGPositionCreator:
    """
    Class for creating the positions for plotting the Flood Wave Graph subgraph along a path
    in the Water Network Graph.
    """
    def __init__(self, fwg_subgraph: nx.DiGraph, wng_path: nx.DiGraph):
        """
        Constructor.
        :param x.DiGraph fwg_subgraph: the FWG subgraph along a path in the WNG
        :param x.DiGraph wng_path: the path in the WNG
        """
        self.fwg_subgraph = fwg_subgraph
        self.reg_numbers = list(wng_path.nodes())

        self.graph_to_plot = None
        self.positions = None

    def run(self, start_date: str = None, end_date: str = None,
            plot_all: bool = False):
        """
        Run function. Filters the graph between two dates if necessary and creates the positions.
        :param str start_date: start date of the plot
        :param str end_date: end date of the plot
        :param bool plot_all: whether to plot the whole graph or not
        """
        if not plot_all:
            self.graph_to_plot = self.cut_graph(start_date=start_date, end_date=end_date)
        else:
            self.graph_to_plot = self.fwg_subgraph

        self.positions = self.create_positions(graph=self.graph_to_plot)

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

    def create_positions(self, graph: nx.DiGraph) -> dict:
        """
        Creates positions. x coordinates are dates with a frequency of 1 day, y coordinates
        are reg-numbers in order
        :param nx.DiGraph graph: graph to plot
        :return dict: the positions in a dictionary, keys are the nodes and values are
        the positions
        """
        min_date_temp = min([node[1] for node in graph.nodes()])
        min_date = datetime.strptime(min_date_temp, '%Y-%m-%d')

        positions = dict()
        for node in graph.nodes():
            x_coord = (datetime.strptime(node[1], '%Y-%m-%d') - min_date).days - 1
            y_coord = len(self.reg_numbers) - self.reg_numbers.index(node[0])
            positions[node] = (x_coord, y_coord)

        return positions
