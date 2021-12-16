from typing import List

from com.github.xadkile.bicp.doc.data_structure.cell.Cell import Cell
from com.github.xadkile.bicp.doc.data_structure.cell.address.CellAddress import CellAddress
from com.github.xadkile.bicp.doc.data_structure.range.Range import Range
from com.github.xadkile.bicp.doc.data_structure.range.RangeAddress import RangeAddress
from com.github.xadkile.bicp.doc.data_structure.range.RangeImp import RangeImp
from com.github.xadkile.bicp.doc.data_structure.sheet.Worksheet import Worksheet


class WorksheetImp(Worksheet):

    def __init__(self, colDict=None):

        if colDict is None:
            colDict = {}

        if isinstance(colDict,dict):
            self.__colDict = colDict
        else:
            raise ValueError("colDict must be a dict")


    ### Worksheet ###

    def cell(self, index:CellAddress)->Cell:
        return self.__colDict[index.colIndex].getCell(index)

    def range(self, fromCell: CellAddress, toCell: CellAddress) -> Range:
        return RangeImp(fromCell, toCell, self)

    def col(self,colIndex:int)->Range:
        return self.__colDict[colIndex]

    def row(self,rowIndex:int)->Range:
        pass

    ### MutableCellContainer ###

    def addCell(self, cell: Cell):
        super().addCell(cell)

    def removeCell(self, address: CellAddress):
        super().removeCell(address)

    ### CellContainer ###

    def hasCellAt(self, address: CellAddress) -> bool:
        return super().hasCellAt(address)

    def getCell(self, address: CellAddress) -> Cell:
        return super().getCell(address)

    def isEmpty(self) -> bool:
        return super().isEmpty()

    def containsAddress(self, address: CellAddress) -> bool:
        return super().containsAddress(address)

    @property
    def cells(self) -> List[Cell]:
        return super().cells()

    @property
    def rangeAddress(self) -> RangeAddress:
        return super().rangeAddress()



