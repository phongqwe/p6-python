from com.github.xadkile.bicp.doc.data_structure.cell.Cell import Cell
from com.github.xadkile.bicp.doc.data_structure.cell.TempCell import TempCell
from com.github.xadkile.bicp.doc.data_structure.cell.position.CellPosition import CellPosition
from com.github.xadkile.bicp.doc.data_structure.cell_container.CellContainer import CellContainer


class Column(CellContainer):
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

    def addCell(self, cell: Cell):
        if cell.pos.getColIndex() == self.__colIndex:
            self.__cellDict[cell.pos.getRowIndex()] = cell
        else:
            raise ValueError("cell is in col {wrcol}, can't be inserted into col {ccol} ".format(ccol=self.__colIndex, wrcol=cell.pos.getColIndex()))

    def removeCell(self, pos:CellPosition):
        del self.__cellDict[pos.getRowIndex()]

    def hasCellAt(self, pos:CellPosition):
        return pos.getRowIndex() in self.__cellDict.keys()

    def getCell(self, pos:CellPosition) -> Cell:
        """
        :param pos:
        :return: either the cell at the input position or a TempCell with the same position
        """
        if self.hasCellAt(pos):
            return self.__cellDict[pos.getRowIndex()]
        else:
            return TempCell(self,pos)

    def isEmpty(self):
        return not bool(self.__cellDict)

