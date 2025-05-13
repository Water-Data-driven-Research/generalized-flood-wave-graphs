import pandas as pd


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
        - 'reg_rkm_mapping'
        """
        self.time_series_data = pd.DataFrame()
        self.reg_station_mapping = dict()
        self.station_reg_mapping = dict()
        self.station_coordinates = dict()
        self.river_station_mapping = dict()
        self.station_river_mapping = dict()
        self.river_connections = dict()
        self.reg_rkm_mapping = dict()

        if data is not None:
            for key, value in data.items():
                setattr(self, key, value)
