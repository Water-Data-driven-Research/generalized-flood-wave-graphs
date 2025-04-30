from typing import Tuple

import numpy as np
import pandas as pd

from src.analysis.static.flood_wave_analyser import FloodWaveAnalyser
from src.analysis.static.flood_wave_extractor import FloodWaveExtractor
from src.analysis.static.flood_wave_extractor_interface import FloodWaveExtractorInterface
from src.analysis.static.flood_wave_selector import FloodWaveSelector
from src.analysis.dynamic.wng_path_fwg_selector import WNGPathFWGSelector
from src.data_handling.data_downloader import DataDownloader
from src.data_handling.data_handler import DataHandler
from src.data_handling.data_interface import DataInterface
from src.data_handling.dataloader import DataLoader
from src.fwg_building.flood_wave_graph_builder import FloodWaveGraphBuilder
from src.fwg_building.flood_wave_graph_preparer import FloodWaveGraphPreparer
from src.wng_building.station_river_creator import StationRiverCreator
from src.wng_building.station_river_data_interface import StationRiverDataInterface
from src.wng_building.water_network_graph_builder import WaterNetworkGraphBuilder


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

    expected_nodes = [('1111', '2000-01-06', 130), ('1111', '2000-01-10', 130),
                      ('1111', '2000-01-13', 120), ('2222', '2000-01-07', 130),
                      ('2222', '2000-01-10', 130), ('2222', '2000-01-13', 140)]

    expected_edges = [(('1111', '2000-01-06', 130), ('2222', '2000-01-07', 130)),
                      (('1111', '2000-01-10', 130), ('2222', '2000-01-10', 130)),
                      (('1111', '2000-01-10', 130), ('2222', '2000-01-13', 140)),
                      (('1111', '2000-01-13', 120), ('2222', '2000-01-13', 140))]

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
        folder_link='https://drive.google.com/drive/folders/1CzKFN06mQaku1db9e_zv05JCc4x--NKW?usp=drive_link',
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
        fwg_data_if=fwg_builder.fwg_if,
        wng_data_if=wng_builder.wng_if
    )
    path_selector.run(temporal_filtering=temporal_filtering, spatial_filtering=spatial_filtering)

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


def test_flood_wave_extractor():
    spatial_filtering = {
        'source': '1514',
        'target': '1520',
        'through': []
    }

    temporal_filtering = {
        'start_date': '2016-02-01',
        'end_date': '2016-02-15'
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
        fwg_data_if=fwg_builder.fwg_if,
        wng_data_if=wng_builder.wng_if
    )
    path_selector.run(temporal_filtering=temporal_filtering, spatial_filtering=spatial_filtering)

    extractor = FloodWaveExtractor(
        fwg=path_selector.fwg_subgraph,
        wng=path_selector.wng_subgraph,
        data_if=data_handler.data_if,
        is_equivalence_applied=True,
        do_save_flood_waves=False,
        data_folder_path=ddl.data_folder_path
    )
    extractor.run()

    expected_flood_waves = [
        [('1514', '2016-02-01', -52), ('1515', '2016-02-02', 64),
         ('1516', '2016-02-02', 182), ('171517', '2016-02-05', 161),
         ('1518', '2016-02-07', 520), ('1520', '2016-02-07', 381)],
        [('1514', '2016-02-01', -52), ('1515', '2016-02-02', 64),
         ('1516', '2016-02-02', 182), ('171517', '2016-02-02', 130)],
        [('1514', '2016-02-05', -2), ('1515', '2016-02-05', 201),
         ('1516', '2016-02-06', 318)],
        [('1514', '2016-02-12', -2), ('1515', '2016-02-12', 191),
         ('1516', '2016-02-13', 227)]
    ]

    assert extractor.extractor_if.flood_waves == expected_flood_waves, \
        'FloodWaveExtractor is not working properly.'


def test_flood_wave_selection_by_impacted_stations():
    waves = [
        [('1514', '2016-02-01', -52), ('1515', '2016-02-02', 64),
         ('1516', '2016-02-02', 182), ('171517', '2016-02-05', 161),
         ('1518', '2016-02-07', 520), ('1520', '2016-02-07', 381)],
        [('1514', '2016-02-01', -52), ('1515', '2016-02-02', 64),
         ('1516', '2016-02-02', 182), ('171517', '2016-02-02', 130)],
        [('1514', '2016-02-05', -2), ('1515', '2016-02-05', 201),
         ('1516', '2016-02-06', 318)],
        [('1514', '2016-02-12', -2), ('1515', '2016-02-12', 191),
         ('1516', '2016-02-13', 227)]
    ]
    impacted_stations = ['1515', '171517']

    expected_filtered_waves = [
        [('1514', '2016-02-01', -52), ('1515', '2016-02-02', 64),
         ('1516', '2016-02-02', 182), ('171517', '2016-02-05', 161),
         ('1518', '2016-02-07', 520), ('1520', '2016-02-07', 381)],
        [('1514', '2016-02-01', -52), ('1515', '2016-02-02', 64),
         ('1516', '2016-02-02', 182), ('171517', '2016-02-02', 130)]
    ]

    waves_without_equivalence = [
        [[('1514', '2016-02-01', -52), ('1515', '2016-02-02', 64),
         ('1516', '2016-02-02', 182), ('171517', '2016-02-05', 161),
         ('1518', '2016-02-07', 520), ('1520', '2016-02-07', 381)],
         [('1514', '2016-02-01', -50), ('1515', '2016-02-03', 70),
          ('1516', '2016-02-03', 180), ('171517', '2016-02-06', 150),
          ('1518', '2016-02-06', 500), ('1520', '2016-02-07', 400)]],
        [[('1514', '2016-02-01', -52), ('1515', '2016-02-02', 64),
         ('1516', '2016-02-02', 182), ('171517', '2016-02-02', 130)],
         [('1514', '2016-02-01', -50), ('1515', '2016-02-01', 60),
          ('1516', '2016-02-01', 160), ('171517', '2016-02-02', 135)]]
    ]
    impacted_stations_2 = ['1518']

    expected_filtered_waves_without_equivalence = [
        [[('1514', '2016-02-01', -52), ('1515', '2016-02-02', 64),
         ('1516', '2016-02-02', 182), ('171517', '2016-02-05', 161),
         ('1518', '2016-02-07', 520), ('1520', '2016-02-07', 381)],
         [('1514', '2016-02-01', -50), ('1515', '2016-02-03', 70),
          ('1516', '2016-02-03', 180), ('171517', '2016-02-06', 150),
          ('1518', '2016-02-06', 500), ('1520', '2016-02-07', 400)]]
    ]

    filtered_waves = FloodWaveSelector.get_flood_waves_by_impacted_stations(
        waves=waves,
        impacted_stations=impacted_stations,
        is_equivalence_applied=True
    )

    filtered_waves_without_equivalence = FloodWaveSelector.get_flood_waves_by_impacted_stations(
        waves=waves_without_equivalence,
        impacted_stations=impacted_stations_2,
        is_equivalence_applied=False
    )

    assert filtered_waves == expected_filtered_waves, 'Station filtering with equivalence is not working.'

    error_msg = 'Station filtering without equivalence is not working.'
    assert filtered_waves_without_equivalence == expected_filtered_waves_without_equivalence, error_msg


def test_flood_wave_selection_by_duration():
    waves = [
        [('1514', '2016-02-01', -52), ('1515', '2016-02-02', 64),
         ('1516', '2016-02-02', 182), ('171517', '2016-02-05', 161),
         ('1518', '2016-02-07', 520), ('1520', '2016-02-07', 381)],
        [('1514', '2016-02-01', -52), ('1515', '2016-02-02', 64),
         ('1516', '2016-02-02', 182), ('171517', '2016-02-02', 130)],
        [('1514', '2016-02-05', -2), ('1515', '2016-02-05', 201),
         ('1516', '2016-02-06', 318)],
        [('1514', '2016-02-12', -2), ('1515', '2016-02-12', 191),
         ('1516', '2016-02-13', 227)]
    ]
    duration = 1
    expected_filtered_waves = [
        [('1514', '2016-02-01', -52), ('1515', '2016-02-02', 64),
         ('1516', '2016-02-02', 182), ('171517', '2016-02-02', 130)],
        [('1514', '2016-02-05', -2), ('1515', '2016-02-05', 201),
         ('1516', '2016-02-06', 318)],
        [('1514', '2016-02-12', -2), ('1515', '2016-02-12', 191),
         ('1516', '2016-02-13', 227)]
    ]

    waves_without_equivalence = [
        [[('1514', '2016-02-01', -52), ('1515', '2016-02-02', 64),
         ('1516', '2016-02-02', 182), ('171517', '2016-02-05', 161),
         ('1518', '2016-02-07', 520), ('1520', '2016-02-07', 381)],
         [('1514', '2016-02-01', -50), ('1515', '2016-02-03', 70),
          ('1516', '2016-02-03', 180), ('171517', '2016-02-06', 150),
          ('1518', '2016-02-06', 500), ('1520', '2016-02-07', 400)]],
        [[('1514', '2016-02-01', -52), ('1515', '2016-02-02', 64),
         ('1516', '2016-02-02', 182), ('171517', '2016-02-02', 130)],
         [('1514', '2016-02-01', -50), ('1515', '2016-02-01', 60),
          ('1516', '2016-02-01', 160), ('171517', '2016-02-02', 135)]]
    ]
    duration_2 = 6

    filtered_waves = FloodWaveSelector.get_flood_waves_by_duration(
        waves=waves,
        max_duration_days=duration,
        is_equivalence_applied=True
    )

    filtered_waves_without_equivalence = FloodWaveSelector.get_flood_waves_by_duration(
        waves=waves_without_equivalence,
        max_duration_days=duration_2,
        is_equivalence_applied=False
    )

    assert filtered_waves == expected_filtered_waves, 'Duration filtering with equivalence is not working.'

    error_msg = 'Duration filtering without equivalence is not working.'
    assert filtered_waves_without_equivalence == waves_without_equivalence, error_msg


def test_flood_wave_analyser():
    flood_waves = [
        [('1514', '2016-02-01', -52), ('1515', '2016-02-02', 64),
         ('1516', '2016-02-02', 182), ('171517', '2016-02-05', 161),
         ('1518', '2016-02-07', 520), ('1520', '2016-02-07', 381)],
        [('1514', '2016-02-01', -52), ('1515', '2016-02-02', 64),
         ('1516', '2016-02-02', 182), ('171517', '2016-02-02', 130)],
        [('1514', '2016-02-05', -2), ('1515', '2016-02-05', 201),
         ('1516', '2016-02-06', 318)],
        [('1514', '2016-02-12', -2), ('1515', '2016-02-12', 191),
         ('1516', '2016-02-13', 227)]
    ]

    expected_spatial_lengths = [6, 4, 3, 3]
    expected_durations = [6, 1, 1, 1]

    extractor_if = FloodWaveExtractorInterface()
    extractor_if.flood_waves = flood_waves

    analyser = FloodWaveAnalyser(
        extractor_if=extractor_if,
        is_equivalence_applied=True
    )
    analyser.run()

    assert analyser.spatial_lengths == expected_spatial_lengths, 'Spatial lengths do not match.'

    assert analyser.durations == expected_durations, 'Durations do not match.'
