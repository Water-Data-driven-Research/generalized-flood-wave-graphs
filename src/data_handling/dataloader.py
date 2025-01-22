import json
import os

import gdown
import pandas as pd

from src import PROJECT_PATH


class DataLoader:
    def __init__(self):
        self.dataset_name = 'time_series_data'

        self.download_data()

        self.time_series_data = None
        self.meta_data = None
        self.river_connections = None
        self.read_data()

    def download_data(self) -> None:
        """
        Downloads all data from Google Drive.
        """
        if not self.do_all_files_exist():
            url = "https://drive.google.com/drive/folders/1mPNd7M4s_LPvGGIKP3-2HyiSVUAe5cbl"
            output = os.path.join(PROJECT_PATH, 'data')
            gdown.download_folder(url=url, output=output)

    @staticmethod
    def do_all_files_exist() -> bool:
        """
        This function checks whether all the files we wish to download already exist
        :return bool: True if all of them exist, False if at least one is missing
        """
        files = ["time_series_data.csv", "meta.csv", "river_connections.json"]

        for file in files:
            if not os.path.exists(os.path.join(PROJECT_PATH, 'data', file)):
                return False

        return True

    def read_data(self) -> None:
        """
        Reads downloaded data from the data folder and saves them in member variables.
        """
        self.time_series_data = pd.read_csv(
            os.path.join(PROJECT_PATH, 'data', 'time_series_data.csv'),
            index_col=[0]
        )

        self.meta_data = pd.read_csv(
            os.path.join(PROJECT_PATH, 'data', 'meta_data.csv'),
            index_col=[0]
        )

        with open(
                os.path.join(PROJECT_PATH, 'data', 'river_connections.json')
        ) as f:
            self.river_connections = json.load(f)
