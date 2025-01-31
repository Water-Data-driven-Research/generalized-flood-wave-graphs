import pandas as pd

from src.data_handling.data_interface import DataInterface
from src.data_handling.dataloader import DataLoader


class DataHandler:
    """
    Class for collecting and handling all downloaded data.
    """

    def __init__(self, dl: DataLoader):
        """
        Constructor. We create the following data structures.

        - time_series_data: Pandas DataFrame containing all water level time series data. The
        indices are dates and the column names are station reg-numbers.

        - reg_station_mapping: Dictionary: keys are station reg-numbers, values are station names

        - station_reg_mapping: Dictionary: keys are station names, values are station reg-numbers

        - station_coordinates: Dictionary: keys are station reg-numbers, values are dictionaries
        like {'EOVx': 101317.2, 'EOVy': 735218.1, 'null_point': 73.7} (for Szeged)

        - rivers_station_mapping: Dictionary: keys are river names and values are lists of station
        names lying along the river

        - station_river_mapping: Dictionary: keys are station names and values are the corresponding
        river names

        - river_connections: Dictionary: keys are river names, values are dictionaries
        like {"close_beginning": 0, "close_ending": 2275} (if the river has to be closed
        with station 2275)

        :param DataLoader dl: a DataLoader instance
        """

        self.interface = DataInterface()

        self.run(dl=dl)

    def run(self, dl: DataLoader) -> None:
        """
        Run function. Gets all data structures described in the constructor.
        :param DataLoader dl: a DataLoader instance
        """
        self.interface.time_series_data = dl.time_series_data.astype(pd.Int64Dtype())
        self.interface.reg_station_mapping = dict(dl.meta_data['station_name'])
        self.interface.station_reg_mapping = \
            {v: k for k, v in self.interface.reg_station_mapping.items()}
        self.interface.station_coordinates = self.get_station_coordinates(dl=dl)
        self.interface.river_station_mapping = self.get_river_station_mapping(dl=dl)
        self.interface.station_river_mapping = self.get_station_river_mapping()
        self.interface.river_connections = dl.river_connections

    @staticmethod
    def get_station_coordinates(dl: DataLoader) -> dict:
        """
        Creates the station_coordinates dictionary described in the constructor.
        :return dict: the station coordinates dictionary
        """
        station_coordinates_df = dl.meta_data[['EOVx', 'EOVy', 'null_point']]

        station_coordinates_dict = station_coordinates_df.to_dict(orient='index')

        return station_coordinates_dict

    @staticmethod
    def get_river_station_mapping(dl: DataLoader) -> dict:
        """
        Creates the river-station mapping dictionary described in the constructor.
        :return dict: river-station mapping
        """
        all_river_names = dl.meta_data['river'].values

        river_names_without_duplicates = list(
            dict.fromkeys(all_river_names)
        )

        river_station_mapping = {}
        for river_name in river_names_without_duplicates:
            select_river = dl.meta_data[
                dl.meta_data['river'] == river_name
                ]
            station_names_along_river = list(select_river.station_name.values)

            river_station_mapping[river_name] = station_names_along_river

        return river_station_mapping

    def get_station_river_mapping(self) -> dict:
        """
        Creates the station-river mapping described in the constructor.
        :return dict: station_river_mapping
        """
        station_river_mapping = {}
        for station_name in list(self.interface.reg_station_mapping.values()):
            for river_name in list(self.interface.river_station_mapping.keys()):
                if station_name in self.interface.river_station_mapping[river_name]:
                    station_river_mapping[station_name] = river_name
                    break

        return station_river_mapping
