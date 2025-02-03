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
        if data is not None:
            for key, value in data.items():
                setattr(self, key, value)
