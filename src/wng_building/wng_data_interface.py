import networkx as nx


class WNGDataInterface:
    """
    Class for storing data structures created in WaterNetworkGraphBuilder.
    """
    def __init__(self, data: dict = None):
        """
        Constructor.
        :param data: dictionary containing some data structures. The keys of the dictionary
        represent the data structures. The expected keys are
        - 'vertices'
        - 'river_edges'
        - 'completed_river_edges'
        - 'water_network_graph'
        """
        self.vertices = []
        self.river_edges = {}
        self.completed_river_edges = {}
        self.water_network_graph = nx.DiGraph()

        if data is not None:
            for key, value in data.items():
                setattr(self, key, value)
