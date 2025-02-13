class FWGSelector:
    """
    Class for spatial and temporal filtering of the Flood Wave Graph.
    """
    def __init__(self, graphs: dict, spatial_filtering: dict, temporal_filtering: dict):
        """
        Constructor.
        :param dict graphs: {'fwg': flood_wave_graph, 'wng': water_network_graph}
        :param dict temporal_filtering: {'start_date': start_date, 'end_date': end_date}
        """
        self.graphs = graphs
        self.spatial_filtering = spatial_filtering
        self.temporal_filtering = temporal_filtering

    def run(self):
        pass
