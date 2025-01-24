import json
import os

import gdown
import pandas as pd

from src import PROJECT_PATH


class DataLoader:
    def __init__(self, do_download: bool = False, folder_link: str = ''):
        """
        Constructor.
        :param bool do_download: True if we wish to download data, False if we don't
        :param str folder_link: The link of the folder containing all necessary data
        """
        self.folder_link = folder_link
        self.dataset_name = 'time_series_data'

        if do_download:
            self.download_data()

        self.time_series_data = None
        self.meta_data = None
        self.river_connections = None
        self.read_data()

    def download_data(self) -> None:
        """
        Downloads all data from Google Drive.
        """
        output = os.path.join(PROJECT_PATH, 'data')
        gdown.download_folder(url=self.folder_link, output=output)

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
            index_col=[5]
        )

        with open(
                os.path.join(PROJECT_PATH, 'data', 'river_connections.json')
        ) as f:
            self.river_connections = json.load(f)
