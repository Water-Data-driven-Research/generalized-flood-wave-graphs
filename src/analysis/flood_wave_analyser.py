from datetime import datetime

import numpy as np

from src.data_handling.generated_dataloader import GeneratedDataLoader


class FloodWaveAnalyser:
    """
    Class for analysing flood waves.
    """
    def __init__(self, flood_waves: list = None, is_equivalence_applied: bool = None,
                 data_folder_path: str = None, wave_folder_name: str = None):
        """
        Constructor. Either pass flood_waves and is_equivalence_applied, or let the constructor
        load these data with the help of data_folder_path and wave_folder_name.
        :param list flood_waves: list of all flood waves we wish to analyse
        :param bool is_equivalence_applied: True if we only consider one element of the equivalence
        classes, False otherwise
        :param str data_folder_path: path of the data folder
        :param str wave_folder_name: name of the folder containing the waves file
        """
        if flood_waves is not None:
            self.flood_waves = flood_waves
            self.is_equivalence_applied = is_equivalence_applied
        else:
            self.data_folder_path = data_folder_path
            waves = GeneratedDataLoader.read_json(
                data_folder_path=self.data_folder_path,
                subfolder_names=['flood_waves', wave_folder_name],
                file_name='waves'
            )

            self.flood_waves = waves['flood_waves']
            self.is_equivalence_applied = waves['is_equivalence_applied']

        if self.is_equivalence_applied:
            self.flood_waves_to_analyse = self.flood_waves
        else:
            self.flood_waves_to_analyse = [wave for paths in self.flood_waves for wave in paths]

    def run(self) -> dict:
        """
        Run function. Gets the number of flood waves total, gets spatial and temporal lengths
        of flood waves.
        :return dict: dictionary containing the results
        """
        number_of_flood_waves = len(self.flood_waves_to_analyse)
        spatial_lengths = self.get_spatial_lengths()
        temporal_lengths = self.get_temporal_lengths()

        results = {
            'number_of_flood_waves': number_of_flood_waves,
            'spatial_statistics': self.get_statistics(data=np.array(spatial_lengths)),
            'temporal_statistics': self.get_statistics(data=np.array(temporal_lengths))
        }

        return results

    def get_spatial_lengths(self) -> list:
        """
        Collects spatial lengths of all flood waves in a list.
        :return list: spatial lengths of all flood waves
        """
        spatial_lengths = []
        for wave in self.flood_waves_to_analyse:
            spatial_lengths.append(len(wave))

        return spatial_lengths

    def get_temporal_lengths(self) -> list:
        """
        Collects temporal lengths of all flood waves in a list.
        :return list: temporal lengths of all flood waves
        """
        temporal_lengths = []
        for wave in self.flood_waves_to_analyse:
            date1 = datetime.strptime(wave[0][1], "%Y-%m-%d")
            date2 = datetime.strptime(wave[-1][1], "%Y-%m-%d")
            days_diff = (date2 - date1).days
            temporal_lengths.append(days_diff)

        return temporal_lengths

    @staticmethod
    def get_statistics(data: np.ndarray) -> dict:
        """
        Gathers basic statistics of some numerical data.
        :param np.array data: spatial or temporal lengths
        :return dict: dictionary of basic statistics
        """
        stats = {
            'mean': np.mean(data),
            'median': np.median(data),
            'max': np.max(data),
            'min': np.min(data)
        }

        return stats
