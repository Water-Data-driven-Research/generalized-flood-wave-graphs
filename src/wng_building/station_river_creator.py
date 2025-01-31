import copy

from src.data_handling.data_interface import DataInterface
from src.wng_building.station_river_data_interface import StationRiverDataInterface


class StationRiverCreator:
    """
    Class for creating the following data structures: stations, rivers, completed rivers
    """
    def __init__(self, data_interface: DataInterface):
        """
        Constructor.
        :param DataInterface data_interface: a DataInterface instance
        """
        self.data = data_interface

        self.interface = StationRiverDataInterface()

    def run(self) -> None:
        """
        Run function. Gets stations, rivers and completed rivers.
        """

        self.create_stations()

        self.create_rivers()

        self.create_completed_rivers()

    def create_stations(self) -> None:
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
        """
        stations = {}
        for reg_num in list(self.data.reg_station_mapping.keys()):
            station_name = self.data.reg_station_mapping[reg_num]
            river_name = self.data.station_river_mapping[station_name]

            stations[reg_num] = {
                'river_name': river_name,
                'station_name': station_name,
                'EOVy': self.data.station_coordinates[reg_num]['EOVy'],
                'EOVx': self.data.station_coordinates[reg_num]['EOVx'],
                'null_point': self.data.station_coordinates[reg_num]['null_point']
            }

        self.interface.stations = stations

    def create_rivers(self) -> None:
        """
        Function for creating the rivers data structure. A river looks like
        {'river_name': [station1, station2, ..., stationN]}, where the stations
        inside the list are sorted in descending order by their null points.
        """
        rivers_unsorted = self.get_rivers_unsorted()
        rivers_sorted = self.sort_rivers(rivers_unsorted=rivers_unsorted)

        self.interface.rivers = rivers_sorted

    def create_completed_rivers(self) -> None:
        """
        Creates completed rivers. Uses river_connections to append the rivers with some
        "completing" stations.
        """
        completed_rivers = copy.deepcopy(self.interface.rivers)
        for river_name in list(self.data.river_connections.keys()):
            close_beginning = self.data.river_connections[river_name]['close_beginning']
            close_ending = self.data.river_connections[river_name]['close_ending']

            if close_beginning is not None:
                completed_rivers[river_name] = [close_beginning] + completed_rivers[river_name]
            if close_ending is not None:
                completed_rivers[river_name] = completed_rivers[river_name] + [close_ending]

        self.interface.completed_rivers = completed_rivers

    def get_rivers_unsorted(self) -> dict:
        """
        Creates dictionary of dictionaries like
        {'river_name': [station1, station2, ..., stationN]}, where the stations
        inside the list are not sorted.
        :return dict: dictionary of unsorted rivers
        """
        rivers_unsorted = {}
        for river_name in list(self.data.river_station_mapping.keys()):
            station_name_list = self.data.river_station_mapping[river_name]
            reg_number_list = [
                self.data.station_reg_mapping[station_name] for station_name in station_name_list
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
                key=lambda x: -self.data.station_coordinates[x]['null_point']
            )

            rivers_sorted[river_name] = river_sorted

        return rivers_sorted
