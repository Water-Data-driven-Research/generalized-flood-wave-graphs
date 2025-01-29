from src.data_handling.data_handler import DataHandler
from src.data_handling.dataloader import DataLoader
from src.data_handling.generated_data_handler import GeneratedDataHandler
from src.wng_building.station_river_creator import StationRiverCreator


class WaterNetworkGraphBuilder:
    def __init__(self, dl: DataLoader):
        self.dl = dl

        self.data_handler = DataHandler(dl=self.dl)
        self.station_river_creator = StationRiverCreator(data_handler=self.data_handler)

    def run(self):
        self.station_river_creator.run()

        self.get_vertices()

    def get_vertices(self):
        vertices = list(self.station_river_creator.stations.keys())

        GeneratedDataHandler.save_pickle(
            vertices=vertices, edges=[],
            data_folder_path=self.dl.data_folder_path,
            file_name='vertices'
        )
