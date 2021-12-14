from com.github.xadkile.bicp.doc.data_structure.cell.position.CellPosition import CellPosition


class IndexCellPosition(CellPosition):
    def __init__(self, colIndex: int, rowIndex: int):
        self.__rowIndex = rowIndex
        self.__colIndex = colIndex

    def getRowIndex(self) -> int:
        return self.__rowIndex

    def getColIndex(self) -> int:
        return self.__colIndex
    @staticmethod
    def zero()->CellPosition:
        return IndexCellPosition(0,0)