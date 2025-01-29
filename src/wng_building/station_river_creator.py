from src.data_handling.data_handler import DataHandler


class StationRiverCreator:
    def __init__(self, data_handler: DataHandler):
        self.data_handler = data_handler

    def run(self):
        stations = self.create_stations()

    def create_stations(self):
        stations = {}
        for reg_num in list(self.data_handler.station_names.keys()):
            station_name = self.data_handler.station_names[reg_num]
            river_name = self.data_handler.station_river_mapping[station_name]

            stations[reg_num] = {
                'river_name': river_name,
                'station_name': station_name,
                'EOVy': self.data_handler.station_coordinates['EOVy'],
                'EOVx': self.data_handler.station_coordinates['EOVx'],
                'null_point': self.data_handler.station_coordinates['null_point']
            }

        return stations
