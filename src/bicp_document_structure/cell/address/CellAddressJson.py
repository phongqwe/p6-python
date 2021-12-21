

class CellAddressJson(dict):
    def __init__(self, col: int, row: int):
        super().__init__()
        self.row = row
        self.col = col
