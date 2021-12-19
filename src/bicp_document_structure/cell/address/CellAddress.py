from abc import ABC


class CellAddress(ABC):
    """
    an interface representing a position of a cell, including row and column index
    """

    @property
    def rowIndex(self) -> int:
        """ read-only row index """
        raise NotImplementedError()

    @property
    def colIndex(self) -> int:
        """ read-only col index """
        raise NotImplementedError()

    def __eq__(self, o) -> bool:
        if isinstance(o, CellAddress):
            sameRow = (self.rowIndex == o.rowIndex)
            sameCol = (self.colIndex == o.colIndex)
            return sameRow and sameCol
        else:
            return False
