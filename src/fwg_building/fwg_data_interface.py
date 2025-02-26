import networkx as nx


class FWGDataInterface:
    """
    Class for storing the Flood Wave Graph.
    """
    def __init__(self):
        """
        Constructor. The only member variable is fwg.
        """
        self.flood_wave_graph = nx.DiGraph()
