import datetime
from itertools import product

import pandas as pd

from src.data_handling.data_interface import DataInterface
from src.fwg_building.fwg_preparer_data_interface import FWGPreparerDataInterface
from src.wng_building.station_river_data_interface import StationRiverDataInterface


class FloodWaveGraphPreparer:
    """
    Class for finding the nodes and edges of the Flood Wave Graph.
    """
    def __init__(self, data_if: DataInterface , station_river_data_if: StationRiverDataInterface,
                 beta: int, delta: int):
        """
        Constructor.
        :param DataInterface data_if: a DataInterface instance
        :param StationRiverDataInterface station_river_data_if: a StationRiverDataInterface instance
        :param int beta: hyperparameter for setting the maximal allowed time difference (in days)
        between two connected nodes
        :param int delta: hyperparameter for setting the lengths of the time intervals in which
        we are looking for a peak value
        """
        self.time_series_data = data_if.time_series_data
        self.completed_rivers = station_river_data_if.completed_rivers
        self.beta = beta
        self.delta = delta

        self.preparer_if = FWGPreparerDataInterface()

    def run(self) -> None:
        """
        Run function. Finds delta peaks and edges and saves them into the member variables
        of the interface.
        """
        delta_peak_bools = self.find_delta_peaks()
        data = {
            'delta_peaks': delta_peak_bools,
            'edges': self.find_edges(delta_peak_bools=delta_peak_bools)
        }

        self.preparer_if = FWGPreparerDataInterface(data=data)

    def find_delta_peaks(self) -> pd.DataFrame:
        """
        Finds delta-peaks using pandas.
        :return pd.DataFrame: Data frame containing True and False values. True means delta-peak,
        False means not delta-peak.
        """
        peaks = pd.DataFrame(
            True,
            index=self.time_series_data.index,
            columns=self.time_series_data.columns
        )

        for i in range(-self.delta, 0):
            peaks = peaks * (self.time_series_data >= self.time_series_data.shift(i))
        for i in range(1, self.delta + 1):
            peaks = peaks * (self.time_series_data > self.time_series_data.shift(i))

        peaks.fillna(value=False, inplace=True)

        return peaks

    def find_edges(self, delta_peak_bools: pd.DataFrame) -> list:
        """
        Finds all edges of the FWG.
        :param pd.DataFrame delta_peak_bools: delta-peaks data frame
        :return list: all edges in a list
        """
        all_edges = []
        for completed_river_name in self.completed_rivers:
            completed_river = self.completed_rivers[completed_river_name]
            peaks_along_completed_river = delta_peak_bools[completed_river]

            edges_along_completed_river = self.find_edges_along_completed_river(
                completed_river=completed_river,
                peaks=peaks_along_completed_river
            )

            all_edges.extend(edges_along_completed_river)

        return all_edges

    def find_edges_along_completed_river(self, completed_river: list, peaks: pd.DataFrame) -> list:
        """
        Finds edges along a single completed river.
        :param list completed_river: sorted list of stations in the completed river
        :param pd.DataFrame peaks: delta-peak data frame
        :return list: edges along the completed river
        """
        final_edges = []
        for start, end in zip(completed_river[:-1], completed_river[1:]):
            start_dates = peaks[start].loc[peaks[start]].index
            end_dates = peaks[end].loc[peaks[end]].index
            for date in start_dates:
                # condition for being an edge
                filtered_ends = end_dates[
                    (date <= end_dates) & \
                    (end_dates <= date + datetime.timedelta(days=self.beta))
                    ]
                filtered_ends_datetime = pd.Series(filtered_ends).apply(
                    lambda x: datetime.datetime.strftime(x, "%Y-%m-%d")
                )
                date_datetime = datetime.datetime.strftime(date, "%Y-%m-%d")

                # final structure of edges
                water_level_at_start_node = int(self.time_series_data[start].loc[date_datetime])
                start_node = [(start, date_datetime, water_level_at_start_node)]
                water_levels_at_end_nodes = list(map(
                    int,
                    list(self.time_series_data[end].loc[filtered_ends_datetime].values)
                ))
                end_nodes = [(end, bi, ci) for bi, ci in zip(filtered_ends_datetime, water_levels_at_end_nodes)]

                edges = list(product(
                    start_node, end_nodes
                ))

                final_edges.extend(edges)

        return final_edges
