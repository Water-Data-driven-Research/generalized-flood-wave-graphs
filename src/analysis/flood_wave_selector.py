from datetime import datetime


class FloodWaveSelector:

    @staticmethod
    def get_flood_waves_by_impacted_stations(waves: list, impacted_stations: list,
                                             is_equivalence_applied: bool) -> list:
        """
        Selects only those flood waves that impacted all stations in impacted_stations.
        :param list waves: list of all the flood waves
        :param list impacted_stations: stations the flood waves should go through
        :param bool is_equivalence_applied: True if we only consider one element of the equivalence
        classes, False otherwise
        :return list: full flood waves
        """
        if is_equivalence_applied:
            final_waves = []
            for wave in waves:
                stations_in_flood_wave = [wave[i][0] for i in range(len(wave))]
                if set(impacted_stations).issubset(stations_in_flood_wave):
                    final_waves.append(wave)

        else:
            final_waves = []
            for paths in waves:
                filtered_paths = []
                for path in paths:
                    stations_in_flood_wave = [path[i][0] for i in range(len(path))]
                    if set(impacted_stations).issubset(stations_in_flood_wave):
                        filtered_paths.append(path)
                        final_waves.append(filtered_paths)

        return final_waves

    @staticmethod
    def get_flood_waves_by_duration(waves: list, max_duration_days: int,
                                    is_equivalence_applied: bool) -> list:
        """
        Gets flood waves for which the time difference between the first and last nodes
        are at most max_duration_days.
        :param list waves: list of all the flood waves
        :param int max_duration_days: maximal allowed time duration of a flood wave
        :param bool is_equivalence_applied: True if we only consider one element of the equivalence
        classes, False otherwise
        :return: flood waves that lasted for at most max_duration_days days
        """
        if is_equivalence_applied:
            final_waves = []
            for wave in waves:
                date1 = datetime.strptime(wave[0][1], "%Y-%m-%d")
                date2 = datetime.strptime(wave[-1][1], "%Y-%m-%d")
                days_diff = (date2 - date1).days
                if days_diff <= max_duration_days:
                    final_waves.append(wave)

        else:
            final_waves = []
            for paths in waves:
                date1 = datetime.strptime(paths[0][0][1], "%Y-%m-%d")
                date2 = datetime.strptime(paths[0][-1][1], "%Y-%m-%d")
                days_diff = (date2 - date1).days
                if days_diff <= max_duration_days:
                    final_waves.append(paths)

        return final_waves
