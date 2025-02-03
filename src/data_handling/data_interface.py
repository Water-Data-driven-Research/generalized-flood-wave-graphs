class DataInterface:
    """
    Class for storing data created in DataHandler.
    """
    def __init__(self, data: dict = None):
        """
        Constructor.
        :param dict data: dictionary containing some data structures. The keys of the dictionary
        represent the data structures. The expected keys are
        - 'time_series_data'
        - 'reg_station_mapping'
        - 'station_reg_mapping'
        - 'station_coordinates'
        - 'river_station_mapping'
        - 'station_river_mapping'
        - 'river_connections'
        """
        self.time_series_data = None
        self.reg_station_mapping = None
        self.station_reg_mapping = None
        self.station_coordinates = None
        self.river_station_mapping = None
        self.station_river_mapping = None
        self.river_connections = None

        if data is not None:
            for key, value in data.items():
                setattr(self, key, value)
