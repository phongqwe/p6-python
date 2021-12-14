from com.github.xadkile.bicp.doc.data_structure.cell.Cell import Cell
from com.github.xadkile.bicp.doc.data_structure.cell.TempCell import TempCell
from com.github.xadkile.bicp.doc.data_structure.cell.position.CellPosition import CellPosition
from com.github.xadkile.bicp.doc.data_structure.cell_holder.CellHolder import CellHolder


class Column(CellHolder):
    """
    Column is a dictionary of cell: rowIndex -> cell
    """
    def __init__(self, colIndex:int,cellDict:dict):
        if type(cellDict) is dict:
            self.__cellDict = cellDict
            self.__colIndex = colIndex
        else:
            raise ValueError("cellDict must be a dict")

    @staticmethod
    def empty(colIndex:int):
        return Column(colIndex,{})

    def setCell(self, pos:CellPosition, cell: Cell):
        # test cell position
        if cell.pos == pos:
            self.__cellDict[pos.getRowIndex()] = cell




    def removeCell(self, pos:CellPosition):
        del self.__cellDict[pos.getRowIndex()]

    def hasCellAt(self, pos:CellPosition):
        return pos.getRowIndex() in self.__cellDict.keys()

    def getCell(self, pos:CellPosition) -> Cell:
        if self.hasCellAt(pos):
            return self.__cellDict[pos.getRowIndex()]
        else:
            return TempCell(self,pos)

    def isEmpty(self):
        """
        :return: true if this row is empty
        """
        return not bool(self.__cellDict)

