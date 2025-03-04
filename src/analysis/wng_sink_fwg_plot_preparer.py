from src.data_handling.data_interface import DataInterface
from src.fwg_building.fwg_data_interface import FWGDataInterface


class WNGSinkFWGPlotPreparer:
    def __init__(self, data_if: DataInterface, fwg_if: FWGDataInterface):
        self.station_coordinates = data_if.station_coordinates
        self.fwg = fwg_if.flood_wave_graph

        self.node_positions = {}
        self.dates_dict = {}

    def run(self):
        self.create_positions_and_get_dates_dict()

    def create_positions_and_get_dates_dict(self):
        for node in self.fwg.nodes:
            base_x = self.station_coordinates[node[0]]['EOVy']
            base_y = self.station_coordinates[node[0]]['EOVx']
            self.node_positions[node] = (base_x, base_y)

            if node[0] not in self.dates_dict.keys():
                self.dates_dict[node[0]] = [node[1]]
            else:
                self.dates_dict[node[0]].append([node[1]])
