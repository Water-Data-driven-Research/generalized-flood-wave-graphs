import pandas as pd


class FWGPreparerDataInterface:
    """
    Class for storing data structures created in FloodWaveGraphPreparer.
    """
    def __init__(self, data: dict = None):
        """
        Constructor.
        :param dict data: dictionary containing some data structures. The keys of the dictionary
        represent the data structures. The expected keys are
        - 'delta_peaks'
        - 'edges'
        """
        self.delta_peaks = pd.DataFrame()
        self.edges = []

        if data is not None:
            for key, value in data.items():
                setattr(self, key, value)
