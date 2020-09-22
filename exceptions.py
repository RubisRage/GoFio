class KoException(Exception):
    pass

class SuicideException(Exception):
    
    def __init__(self):
        super().__init__("Can't place a stone where there are no liberties!")

class OccupiedPositionException(Exception):
    pass