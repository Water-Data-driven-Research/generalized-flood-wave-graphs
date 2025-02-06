import copy

from src.data_handling.data_interface import DataInterface
from src.wng_building.station_river_data_interface import StationRiverDataInterface


class StationRiverCreator:
    """
    Class for creating the following data structures: stations, rivers, completed rivers
    """
    def __init__(self, data_if: DataInterface):
        """
        Constructor.
        :param DataInterface data_if: a DataInterface instance
        """
        self.data_if = data_if

        self.station_river_if = StationRiverDataInterface()

    def run(self) -> None:
        """
        Run function. Gets stations, rivers and completed rivers.
        """
        rivers = self.create_rivers()
        data = {
            'stations': self.create_stations(),
            'rivers': rivers,
            'completed_rivers': self.create_completed_rivers(rivers=rivers)
        }

        self.station_river_if = StationRiverDataInterface(data=data)

    def create_stations(self) -> dict:
        """
        Function for creating the stations data structure.
        stations is a dictionary with reg-number keys and dictionary values like
        2275: {
            'river_name': Tisza,
            'station_name': 'Szeged',
            'EOVy': 735218.1,
            'EOVx': 101317.2,
            'null_point': 73.70
        }
        :return dict: dictionary containing the stations
        """
        stations = {}
        for reg_num in list(self.data_if.reg_station_mapping.keys()):
            station_name = self.data_if.reg_station_mapping[reg_num]
            river_name = self.data_if.station_river_mapping[station_name]

            stations[reg_num] = {
                'river_name': river_name,
                'station_name': station_name,
                'EOVy': self.data_if.station_coordinates[reg_num]['EOVy'],
                'EOVx': self.data_if.station_coordinates[reg_num]['EOVx'],
                'null_point': self.data_if.station_coordinates[reg_num]['null_point']
            }

        return stations

    def create_rivers(self) -> dict:
        """
        Function for creating the rivers data structure. A river looks like
        {'river_name': [station1, station2, ..., stationN]}, where the stations
        inside the list are sorted in descending order by their null points.
        :return dict: dictionary containing the rivers
        """
        rivers_unsorted = self.get_rivers_unsorted()
        rivers_sorted = self.sort_rivers(rivers_unsorted=rivers_unsorted)

        return rivers_sorted

    def create_completed_rivers(self, rivers: dict) -> dict:
        """
        Creates completed rivers. Uses river_connections to append the rivers with some
        "completing" stations.
        :return dict rivers: dictionary containing the rivers
        :return dict: dictionary containing the completed rivers
        """
        completed_rivers = copy.deepcopy(rivers)
        for river_name in list(self.data_if.river_connections.keys()):
            close_beginning = self.data_if.river_connections[river_name]['close_beginning']
            close_ending = self.data_if.river_connections[river_name]['close_ending']

            if close_beginning is not None:
                completed_rivers[river_name] = [close_beginning] + completed_rivers[river_name]
            if close_ending is not None:
                completed_rivers[river_name] = completed_rivers[river_name] + [close_ending]

        return completed_rivers

    def get_rivers_unsorted(self) -> dict:
        """
        Creates dictionary of dictionaries like
        {'river_name': [station1, station2, ..., stationN]}, where the stations
        inside the list are not sorted.
        :return dict: dictionary of unsorted rivers
        """
        rivers_unsorted = {}
        for river_name in list(self.data_if.river_station_mapping.keys()):
            station_name_list = self.data_if.river_station_mapping[river_name]
            reg_number_list = [
                self.data_if.station_reg_mapping[station_name] for station_name in station_name_list
            ]

            rivers_unsorted[river_name] = reg_number_list

        return rivers_unsorted

    def sort_rivers(self, rivers_unsorted: dict) -> dict:
        """
        Sorts stations in rivers in descending order by their null points
        :param dict rivers_unsorted: dictionary of unsorted rivers
        :return dict: dictionary of sorted rivers
        """
        rivers_sorted = {}
        for river_name in list(rivers_unsorted.keys()):
            river_unsorted = rivers_unsorted[river_name]
            river_sorted = sorted(
                river_unsorted,
                key=lambda x: -self.data_if.station_coordinates[x]['null_point']
            )

            rivers_sorted[river_name] = river_sorted

        return rivers_sorted
