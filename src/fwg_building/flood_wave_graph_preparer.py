import datetime
from itertools import product

import pandas as pd

from src.fwg_building.fwg_preparer_data_interface import FWGPreparerDataInterface


class FloodWaveGraphPreparer:
    def __init__(self, time_series_data: pd.DataFrame, completed_rivers: dict,
                 beta: int, delta: int):
        self.time_series_data = time_series_data
        self.completed_rivers = completed_rivers
        self.beta = beta
        self.delta = delta

        self.preparer_if = FWGPreparerDataInterface()

    def run(self):
        delta_peak_bools = self.find_delta_peaks()
        data = {
            'delta_peaks': delta_peak_bools,
            'edges': self.find_edges(delta_peak_bools=delta_peak_bools)
        }

        self.preparer_if = FWGPreparerDataInterface(data=data)

    def find_delta_peaks(self) -> pd.DataFrame:
        peaks = pd.DataFrame(
            True,
            index=self.time_series_data.index,
            columns=self.time_series_data.columns
        )

        for i in range(-self.delta, 0):
            peaks = peaks * (self.time_series_data > self.time_series_data.shift(i))
        for i in range(1, self.delta + 1):
            peaks = peaks * (self.time_series_data >= self.time_series_data.shift(i))

        peaks.fillna(value=False, inplace=True)

        return peaks

    def find_edges(self, delta_peak_bools: pd.DataFrame):
        all_edges = []
        for completed_river_name in self.completed_rivers:
            completed_river = self.completed_rivers[completed_river_name]
            completed_river = list(map(str, completed_river))
            peaks_along_completed_river = delta_peak_bools[completed_river]

            edges_along_completed_river = self.find_edges_along_completed_river(
                completed_river=completed_river,
                peaks=peaks_along_completed_river
            )

            all_edges.extend(edges_along_completed_river)

        return all_edges

    def find_edges_along_completed_river(self, completed_river: list, peaks: pd.DataFrame) -> list:
        edges = []
        for start, end in zip(completed_river[:-1], completed_river[1:]):
            start_dates = peaks[start].loc[peaks[start]].index
            end_dates = peaks[end].loc[peaks[end]].index
            for date in start_dates:
                filtered_ends = end_dates[
                    (date <= end_dates) & \
                    (end_dates <= date + datetime.timedelta(days=self.beta))
                    ]
                filtered_ends_datetime = pd.Series(filtered_ends).apply(
                    lambda x: datetime.datetime.strftime(x, "%Y-%m-%d")
                )
                date_datetime = datetime.datetime.strftime(date, "%Y-%m-%d")

                start_node = [(start, date_datetime)]
                end_nodes = list(product(
                    [end], list(filtered_ends_datetime)
                ))

                final_nodes = list(product(
                    start_node, end_nodes
                ))

                edges.extend(final_nodes)

        return edges
