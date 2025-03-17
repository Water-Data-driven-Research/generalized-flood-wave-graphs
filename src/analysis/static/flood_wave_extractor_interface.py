class FloodWaveExtractorInterface:
    """
    Class for storing the extracted_flood_waves.
    """
    def __init__(self):
        """
        Constructor. The flood_waves member variable stores the extracted flood waves and
        timestamp_folder_name stores the name of the folder where the waves have been saved.
        """
        self.flood_waves = []
        self.timestamp_folder_name = ''
