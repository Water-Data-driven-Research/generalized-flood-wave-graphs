from typing import Tuple

import numpy as np
import pandas as pd

from src.analysis.wng_path_fwg_selector import WNGPathFWGSelector
from src.data_handling.data_downloader import DataDownloader
from src.data_handling.data_handler import DataHandler
from src.data_handling.data_interface import DataInterface
from src.data_handling.dataloader import DataLoader
from src.fwg_building.flood_wave_graph_builder import FloodWaveGraphBuilder
from src.fwg_building.flood_wave_graph_preparer import FloodWaveGraphPreparer
from src.wng_building.station_river_creator import StationRiverCreator
from src.wng_building.station_river_data_interface import StationRiverDataInterface
from src.wng_building.water_network_graph_builder import WaterNetworkGraphBuilder


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


def test_path_selector():
    spatial_filtering = {
        'source': '2753',
        'target': '100283',
        'through': []
    }

    temporal_filtering = {
        'start_date': '2000-01-01',
        'end_date': '2010-01-01'
    }

    ddl = DataDownloader(
        folder_link='https://drive.google.com/drive/folders/1XDQmvYwXSjqXgLu6wZjbxR8ugCSi3Sy5',
        data_folder_path=None
    )

    dl = DataLoader(
        data_folder_path=ddl.data_folder_path
    )

    data_handler = DataHandler(dl=dl)

    station_river_creator = StationRiverCreator(data_if=data_handler.data_if)
    station_river_creator.run()

    wng_builder = WaterNetworkGraphBuilder(
        station_river_if=station_river_creator.station_river_if,
        do_save_all=True,
        data_folder_path=ddl.data_folder_path
    )
    wng_builder.run()

    fwg_preparer = FloodWaveGraphPreparer(
        data_if=data_handler.data_if,
        station_river_data_if=station_river_creator.station_river_if,
        beta=3, delta=2
    )
    fwg_preparer.run()

    fwg_builder = FloodWaveGraphBuilder(
        preparer_interface=fwg_preparer.preparer_if,
        do_save_fwg=True,
        data_folder_path=ddl.data_folder_path
    )
    fwg_builder.run()

    path_selector = WNGPathFWGSelector(
        data_folder_path=ddl.data_folder_path,
        spatial_filtering=spatial_filtering,
        temporal_filtering=temporal_filtering,
        fwg_data_if=fwg_builder.fwg_if,
        wng_data_if=wng_builder.wng_if
    )
    path_selector.run()

    expected_stations = ['2753', '2756', '2759', '2760', '2272', '2274', '2275', '100283']

    assert set(path_selector.wng_subgraph.nodes()) == set(expected_stations), ('The WNG filtering was'
                                                                               'not successful')

    do_all_nodes_pass = True
    for node in path_selector.fwg_subgraph.nodes():
        is_station_in_expected_stations = node[0] in expected_stations
        is_date_valid = '2000-01-01' <= node[1] <= '2010-01-01'
        does_node_pass = is_station_in_expected_stations * is_date_valid

        do_all_nodes_pass = do_all_nodes_pass * does_node_pass

    assert do_all_nodes_pass, 'Some nodes of the FWG do not satisfy the requirements.'

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
