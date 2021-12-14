from collections import defaultdict

from com.github.xadkile.bicp.doc.data_structure.cell.Cell import Cell
from com.github.xadkile.bicp.doc.data_structure.cell.position.CellPosition import CellPosition
from com.github.xadkile.bicp.doc.data_structure.range.Range import Range


class SheetImp:
    """
    Sheet is a dict or Row objects
    """
    # def __init__(self, colDict):
    #     if type(colDict) is defaultdict:
    #         self.__colDict = colDict
    #     else:
    #         raise ValueError("rowDict must be a defaultdict")

    def cell(self,cellPos:CellPosition)->Cell:
        # return self.__colDict[cellPos.getColIndex()].getCell(cellPos)
        pass

    def range(self,colIndex:int, rowIndex:int)->Range:
        pass

    def col(self,colIndex:int)->Range:
        pass

    def row(self,rowIndex:int)->Range:
        pass
