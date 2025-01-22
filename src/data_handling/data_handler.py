import pandas as pd

from src.data_handling.dataloader import DataLoader


class DataHandler:
    def __init__(self, dl: DataLoader):
        self.dl = dl

        self.time_series_data = self.dl.time_series_data.astype(pd.Int64Dtype())
        self.station_names = dict(self.dl.meta_data['station_name'])
        self.station_coordinates = self.get_station_coordinates()
        self.river_names = self.get_river_names()
        self.river_connections = self.dl.river_connections

    def get_river_names(self) -> list:
        all_river_names = self.dl.meta_data['river'].values

        river_names_without_duplicates = list(
            dict.fromkeys(all_river_names)
        )

        return river_names_without_duplicates

    def get_station_coordinates(self) -> dict:
        station_coordinates_df = self.dl.meta_data[['EOVx', 'EOVy', 'null_point']]

        station_coordinates_dict = station_coordinates_df.to_dict(orient='index')

        return station_coordinates_dict
