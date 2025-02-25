from datetime import datetime

import numpy as np


class FloodWaveAnalyser:
    """
    Class for analysing flood waves.
    """
    def __init__(self, flood_waves: list):
        """
        Constructor.
        :param list flood_waves: list of all flood waves we wish to analyse
        """
        self.flood_waves = flood_waves

        if isinstance(self.flood_waves[0][0], tuple):
            self.flood_waves_flattened = self.flood_waves
        elif isinstance(self.flood_waves[0][0], list):
            self.flood_waves_flattened = [wave for paths in self.flood_waves for wave in paths ]
        else:
            raise Exception('Type of flood wave is not valid.')

    def run(self) -> dict:
        """
        Run function. Gets the number of flood waves total, gets spatial and temporal lengths
        of flood waves.
        :return dict: dictionary containing the results
        """
        number_of_flood_waves = len(self.flood_waves_flattened)
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
        for wave in self.flood_waves_flattened:
            spatial_lengths.append(len(wave))

        return spatial_lengths

    def get_temporal_lengths(self) -> list:
        """
        Collects temporal lengths of all flood waves in a list.
        :return list: temporal lengths of all flood waves
        """
        temporal_lengths = []
        for wave in self.flood_waves_flattened:
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
