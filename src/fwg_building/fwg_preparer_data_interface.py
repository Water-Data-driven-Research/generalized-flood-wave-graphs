import pandas as pd


class FWGPreparerDataInterface:
    def __init__(self, data: dict = None):
        self.delta_peaks = pd.DataFrame()
        self.edges = []

        if data is not None:
            for key, value in data.items():
                setattr(self, key, value)
