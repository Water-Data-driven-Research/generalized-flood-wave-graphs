import json
import os

import pandas as pd


class DataLoader:
    """
    Class for loading all necessary data.
    """
    def __init__(self,
                 do_download: bool = False,
                 data_folder_path: str = None):
        """
        Constructor.
        :param bool do_download: True if we wish to download data, False if we don't
        :param str data_folder_path: the location where we wish to place the data folder
        """
        self.do_download = do_download
        self.data_folder_path = data_folder_path

        self.dataset_name = 'time_series_data'

        self.time_series_data = pd.DataFrame()
        self.meta_data = pd.DataFrame()
        self.river_connections = dict()
        self.load_data()

    def load_data(self) -> None:
        """
        Reads downloaded data from the data folder and saves them in member variables.
        """
        time_series_file_name = 'time_series_data.csv'
        meta_file_name = 'meta_data.csv'
        river_connections_file_name = 'river_connections.json'

        self.time_series_data = pd.read_csv(
            os.path.join(self.data_folder_path, time_series_file_name),
            index_col=[0]
        )

        self.meta_data = pd.read_csv(
            os.path.join(self.data_folder_path, meta_file_name),
            index_col=[5]
        )

        with open(
                os.path.join(self.data_folder_path, river_connections_file_name)
        ) as f:
            self.river_connections = json.load(f)
