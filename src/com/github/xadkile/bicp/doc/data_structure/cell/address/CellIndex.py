from com.github.xadkile.bicp.doc.data_structure.cell.address.CellAddress import CellAddress


class CellIndex(CellAddress):
    """ cell address in form of col index and row index """

    def __init__(self, colIndex: int, rowIndex: int):
        self.__rowIndex = rowIndex
        self.__colIndex = colIndex

    @property
    def rowIndex(self) -> int:
        return self.__rowIndex

    @property
    def colIndex(self) -> int:
        return self.__colIndex

    @staticmethod
    def zero() -> CellAddress:
        return CellIndex(0, 0)

    def __str__(self):
        return "CR({col}:{row})".format(col=self.__colIndex, row=self.__rowIndex)
