import copy

from src.data_handling.data_handler import DataHandler


class StationRiverCreator:
    def __init__(self, data_handler: DataHandler):
        self.data_handler = data_handler

        self.stations = None
        self.rivers = None
        self.completed_rivers = None

    def run(self):
        self.stations = self.create_stations()

        self.rivers = self.create_rivers()

        self.completed_rivers = self.create_completed_rivers()

    def create_stations(self) -> dict:
        stations = {}
        for reg_num in list(self.data_handler.reg_station_mapping.keys()):
            station_name = self.data_handler.reg_station_mapping[reg_num]
            river_name = self.data_handler.station_river_mapping[station_name]

            stations[reg_num] = {
                'river_name': river_name,
                'station_name': station_name,
                'EOVy': self.data_handler.station_coordinates[reg_num]['EOVy'],
                'EOVx': self.data_handler.station_coordinates[reg_num]['EOVx'],
                'null_point': self.data_handler.station_coordinates[reg_num]['null_point']
            }

        return stations

    def create_rivers(self) -> dict:
        rivers_unsorted = self.get_rivers_unsorted()

        return self.sort_rivers(rivers_unsorted=rivers_unsorted)

    def get_rivers_unsorted(self) -> dict:
        rivers_unsorted = {}
        for river_name in list(self.data_handler.river_station_mapping.keys()):
            station_name_list = self.data_handler.river_station_mapping[river_name]
            reg_number_list = [
                self.data_handler.station_reg_mapping[station_name] for station_name in station_name_list
            ]

            rivers_unsorted[river_name] = reg_number_list

        return rivers_unsorted

    def sort_rivers(self, rivers_unsorted: dict) -> dict:
        rivers_sorted = {}
        for river_name in list(rivers_unsorted.keys()):
            river_unsorted = rivers_unsorted[river_name]
            river_sorted = sorted(
                river_unsorted,
                key=lambda x: -self.data_handler.station_coordinates[x]['null_point']
            )

            rivers_sorted[river_name] = river_sorted

        return rivers_sorted

    def create_completed_rivers(self) -> dict:
        completed_rivers = copy.deepcopy(self.rivers)
        for river_name in list(self.data_handler.river_connections.keys()):
            close_beginning = self.data_handler.river_connections[river_name]['close_beginning']
            close_ending = self.data_handler.river_connections[river_name]['close_ending']

            if close_beginning != 0:
                completed_rivers[river_name] = [close_beginning] + completed_rivers[river_name]
            if close_ending != 0:
                completed_rivers[river_name] = completed_rivers[river_name] + [close_ending]

        return completed_rivers
