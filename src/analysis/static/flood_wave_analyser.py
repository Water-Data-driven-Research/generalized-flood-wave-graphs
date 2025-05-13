from datetime import datetime

import numpy as np
import pandas as pd

from src.analysis.static.flood_wave_extractor_interface import FloodWaveExtractorInterface
from src.data_handling.data_interface import DataInterface
from src.data_handling.generated_dataloader import GeneratedDataLoader


class FloodWaveAnalyser:
    """
    Class for analysing flood waves.
    """
    def __init__(self, extractor_if: FloodWaveExtractorInterface,
                 data_if: DataInterface,
                 is_equivalence_applied: bool,
                 do_save_results: bool = False, data_folder_path: str = None):
        self.flood_waves = extractor_if.flood_waves
        self.reg_rkm_mapping = data_if.reg_rkm_mapping
        self.is_equivalence_applied = is_equivalence_applied
        self.do_save_results = do_save_results
        self.data_folder_path = data_folder_path
        self.timestamp_folder_name = extractor_if.timestamp_folder_name

        if self.is_equivalence_applied:
            self.flood_waves_to_analyse = self.flood_waves
        else:
            self.flood_waves_to_analyse = [wave for paths in self.flood_waves for wave in paths]

        self.distances = []
        self.durations = []
        self.statistical_results = {}

    def run(self) -> dict:
        """
        Run function. Gets the number of flood waves total, gets distances and durations
        of flood waves. Optionally saves results.
        :return dict: dictionary containing the results
        """
        number_of_flood_waves = len(self.flood_waves_to_analyse)
        self.distances = self.get_distances()
        self.durations = self.get_durations()

        self.statistical_results = {
            'number_of_flood_waves': number_of_flood_waves,
            'spatial_statistics': self.get_statistics(data=np.array(self.distances)),
            'temporal_statistics': self.get_statistics(data=np.array(self.durations))
        }

        if self.do_save_results:
            self.save_results()

        return self.statistical_results

    def get_distances(self) -> list:
        """
        Collects distances of all flood waves in a list.
        :return list: distances of all flood waves
        """
        distances = []
        for wave in self.flood_waves_to_analyse:
            start_station = wave[0][0]
            end_station = wave[-1][0]
            distance = self.reg_rkm_mapping[start_station] - self.reg_rkm_mapping[end_station]
            distances.append(distance)

        return distances

    def get_durations(self) -> list:
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
        :param np.array data: distances or durations
        :return dict: dictionary of basic statistics
        """
        stats = {
            'mean': float(np.mean(data)),
            'median': float(np.median(data)),
            'max': float(np.max(data)),
            'min': float(np.min(data))
        }

        return stats

    def save_results(self) -> None:
        """
        Saves results into the desired folder.
        """
        lengths_and_durations = np.array([self.distances, self.durations]).T
        df = pd.DataFrame(
            data=lengths_and_durations,
            columns=['distances', 'durations'],
            index=range(len(lengths_and_durations))
        )

        GeneratedDataLoader.save_json(
            data=self.statistical_results,
            data_folder_path=self.data_folder_path,
            subfolder_names=['flood_waves', self.timestamp_folder_name],
            file_name='statistical_results'
        )

        GeneratedDataLoader.save_csv(
            data=df,
            data_folder_path=self.data_folder_path,
            subfolder_names=['flood_waves', self.timestamp_folder_name],
            file_name='lengths_and_durations'
        )
