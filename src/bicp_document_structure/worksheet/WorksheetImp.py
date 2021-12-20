from typing import List, Union, Tuple

from bicp_document_structure.cell.Cell import Cell
from bicp_document_structure.cell.address.CellAddress import CellAddress
from bicp_document_structure.cell.address.CellIndex import CellIndex
from bicp_document_structure.cell.address.CellLabel import CellLabel
from bicp_document_structure.column.Column import Column
from bicp_document_structure.column.TempColumn import TempColumn
from bicp_document_structure.range.Range import Range
from bicp_document_structure.range.RangeImp import RangeImp
from bicp_document_structure.range.address.RangeAddress import RangeAddress
from bicp_document_structure.range.address.RangeAddressImp import RangeAddressImp
from bicp_document_structure.range.address.RangeLabel import RangeLabel
from bicp_document_structure.util.Util import typeCheck
from bicp_document_structure.worksheet.Worksheet import Worksheet
from bicp_document_structure.worksheet.WorksheetConst import WorksheetConst


class WorksheetImp(Worksheet):
    def __init__(self, name="", colDict=None):
        if colDict is None:
            colDict = {}
        self.__colDict = colDict
        self.__name = name




    ### >> Worksheet << ###

    @property
    def name(self) -> str:
        return self.__name

    ### >> UserFriendlyWorksheet << ###

    def cell(self, address: Union[str, CellAddress, Tuple[int, int]]) -> Cell:
        parsedAddress = address
        if isinstance(address, str):
            parsedAddress = CellLabel(address)
        if isinstance(address, Tuple):
            parsedAddress = CellIndex(address[0],address[1])
        return self.getCell(parsedAddress)

    def range(self, rangeAddress: Union[str, RangeAddress,Tuple[CellAddress,CellAddress]]) -> Range:
        parsedAddress = rangeAddress
        if isinstance(rangeAddress, str):
            parsedAddress = RangeLabel(rangeAddress)

        if isinstance(rangeAddress,Tuple):
            ad1 = rangeAddress[0]
            ad2 = rangeAddress[1]
            parsedAddress = RangeAddressImp(ad1,ad2)

        return RangeImp.fromRangeAddress(parsedAddress, self)

    ### >> CellContainer << ###

    def isSameRangeAddress(self, other):
        """
        :raise ValueError of other is not a Worksheet
        :param other: other Worksheet
        :return: always return True because every worksheet has the same fixed range address
        """
        typeCheck(other, "other", Worksheet)
        return True

    def hasCellAt(self, address: CellAddress) -> bool:
        typeCheck(address, "address", CellAddress)
        if self.hasColumn(address.colIndex):
            return self.getCol(address.colIndex).hasCellAt(address)
        else:
            return False

    def getCell(self, address: CellAddress) -> Cell:
        col = self.getCol(address.colIndex)
        rt = col.getCell(address)
        return rt

    def isEmpty(self) -> bool:
        return not bool(self.__colDict)

    def containsAddress(self, address: CellAddress) -> bool:
        if self.hasColumn(address.colIndex):
            return self.getCol(address.colIndex).containsAddress(address)
        else:
            return False

    @property
    def cells(self) -> List[Cell]:
        rt = []
        for k, v in (self.__colDict.items()):
            rt.extend(v.cells)
        return rt

    @property
    def rangeAddress(self) -> RangeAddressImp:
        return RangeAddressImp(
            CellIndex(1, 1),
            CellIndex(WorksheetConst.colLimit, WorksheetConst.rowLimit)
        )

    ### >> MutableCellContainer << ###

    def addCell(self, cell: Cell):
        self.getCol(cell.col).addCell(cell)

    def removeCell(self, address: CellAddress):
        col = self.getCol(address.colIndex)
        col.removeCell(address)
        if col.isEmpty():
            self.removeCol(col.index)

    ### >> MutableColumnContainer << ###

    def setCol(self, col: Column):
        if isinstance(col, Column):
            self.__colDict[col.index] = col
        else:
            raise ValueError("input col is not of type Column")

    def removeCol(self, index: int):
        del self.__colDict[index]

    ### >> ColumnContainer << ###

    def hasColumn(self, colIndex: int) -> bool:
        return colIndex in self.__colDict.keys()

    def getCol(self, colIndex: int) -> Column:
        if self.hasColumn(colIndex):
            return self.__colDict[colIndex]
        else:
            return TempColumn(colIndex, self)