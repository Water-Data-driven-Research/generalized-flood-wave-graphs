class StationRiverDataInterface:
    """
    Class for storing data created in StationRiverCreator.
    """
    def __init__(self, data: dict = None):
        """
        Constructor.
        :param dict data: dictionary containing some data structures. The keys of the dictionary
        represent the data structures. The expected keys are
        - 'stations'
        - 'rivers'
        - 'completed_rivers'
        """
        self.stations = dict()
        self.rivers = dict()
        self.completed_rivers = dict()

        if data is not None:
            for key, value in data.items():
                setattr(self, key, value)
