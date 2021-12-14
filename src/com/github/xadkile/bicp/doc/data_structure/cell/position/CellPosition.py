class CellPosition:
    """
    an interface representing a position of a cell
    """

    def getRowIndex(self) -> int:
        pass

    def getColIndex(self) -> int:
        pass

    def __eq__(self, o) -> bool:
        sameRow = (self.getRowIndex() == o.getRowIndex())
        sameCol = (self.getColIndex() == o.getColIndex())
        return sameRow and sameCol
