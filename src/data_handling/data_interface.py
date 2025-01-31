class DataInterface:
    """
    Class for storing data created in DataHandler.
    """
    def __init__(self):
        """
        Constructor.
        """
        self.time_series_data = None
        self.reg_station_mapping = None
        self.station_reg_mapping = None
        self.station_coordinates = None
        self.river_station_mapping = None
        self.station_river_mapping = None
        self.river_connections = None
