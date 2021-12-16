class CellAddress:
    """
    an interface representing a position of a cell, including row and column index
    """

    @property
    def rowIndex(self) -> int:
        """ read-only row index """
        pass

    @property
    def colIndex(self) -> int:
        """ read-only col index """
        pass

    def __eq__(self, o) -> bool:
        sameRow = (self.rowIndex == o.rowIndex)
        sameCol = (self.colIndex == o.colIndex)
        return sameRow and sameCol
