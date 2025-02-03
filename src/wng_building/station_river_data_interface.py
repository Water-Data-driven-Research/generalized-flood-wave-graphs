class StationRiverDataInterface:
    """
    Class for storing data created in StationRiverCreator.
    """
    def __init__(self):
        """
        Constructor.
        """
        self.stations = dict()
        self.rivers = dict()
        self.completed_rivers = dict()
