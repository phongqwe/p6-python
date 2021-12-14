from collections import defaultdict

from com.github.xadkile.bicp.doc.data_structure.cell.Cell import Cell
from com.github.xadkile.bicp.doc.data_structure.column.ColumnImp import Column


class Sheet:
    """
    Sheet is a dict or Row objects
    """

    def __init__(self, colDict):
        if type(colDict) is defaultdict:
            self.__colDict = colDict
        else:
            raise ValueError("rowDict must be a defaultdict")

    def cell(self,colIndex:int,rowIndex:int)->Cell:
        return self.__colDict[colIndex].getCell(rowIndex)


    def range(self,colIndex:int, rowIndex:int)->Range:
        pass

    @property
    def usedRange(self):
        """
        :return: occupied range
        """
        pass
