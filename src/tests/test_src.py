from typing import Tuple

import numpy as np
import pandas as pd

from src.data_handling.data_interface import DataInterface
from src.fwg_building.flood_wave_graph_builder import FloodWaveGraphBuilder
from src.fwg_building.flood_wave_graph_preparer import FloodWaveGraphPreparer
from src.wng_building.station_river_data_interface import StationRiverDataInterface


def test_fwg_building():
    time_series_data, completed_rivers = create_example_data()

    data_if = DataInterface()
    data_if.time_series_data = time_series_data

    station_river_data_if = StationRiverDataInterface()
    station_river_data_if.completed_rivers = completed_rivers

    fwg_preparer = FloodWaveGraphPreparer(
        data_if=data_if,
        station_river_data_if=station_river_data_if,
        beta=3, delta=2
    )
    fwg_preparer.run()

    fwg_builder = FloodWaveGraphBuilder(
        preparer_interface=fwg_preparer.preparer_if
    )
    fwg_builder.run()

    fwg = fwg_builder.fwg_if.flood_wave_graph

    expected_nodes = [('1111', '2000-01-06'), ('1111', '2000-01-10'), ('1111', '2000-01-13'),
                      ('2222', '2000-01-07'), ('2222', '2000-01-10'), ('2222', '2000-01-13')]

    expected_edges = [(('1111', '2000-01-06'), ('2222', '2000-01-07')),
                      (('1111', '2000-01-10'), ('2222', '2000-01-10')),
                      (('1111', '2000-01-10'), ('2222', '2000-01-13')),
                      (('1111', '2000-01-13'), ('2222', '2000-01-13'))]

    assert set(fwg.nodes()) == set(expected_nodes), 'Error while finding delta-peaks'

    assert set(fwg.edges()) == set(expected_edges), 'Error while finding edges'


def create_example_data() -> Tuple[pd.DataFrame, dict]:
    completed_rivers = {
        'c_r': ['1111', '2222']
    }

    ts1 = [100, 100, 120, 120, 120, 130, 100, 100, 100, 130, 100, 110, 120, 120, 120]
    ts2 = [120, 120, 120, 100, 110, 110, 130, 100, 120, 130, 130, 120, 140, 100, 100]

    time_series_data = pd.DataFrame(
        data=np.array([ts1, ts2]).T,
        index=pd.date_range(
            start='2000-01-01',
            end='2000-01-15',
            freq='D'
        ),
        columns=completed_rivers['c_r']
    )

    return time_series_data, completed_rivers
