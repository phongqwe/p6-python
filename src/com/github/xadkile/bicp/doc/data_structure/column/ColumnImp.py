from typing import List

from com.github.xadkile.bicp.doc.data_structure.cell.Cell import Cell
from com.github.xadkile.bicp.doc.data_structure.cell.TempCell import TempCell
from com.github.xadkile.bicp.doc.data_structure.cell.address.CellAddress import CellAddress
from com.github.xadkile.bicp.doc.data_structure.cell.address.CellIndex import CellIndex
from com.github.xadkile.bicp.doc.data_structure.column.Column import Column
from com.github.xadkile.bicp.doc.data_structure.range.Range import Range
from com.github.xadkile.bicp.doc.data_structure.range.RangeAddress import RangeAddress
from com.github.xadkile.bicp.doc.data_structure.range.RangeImp import RangeImp


class ColumnImp(Column):
    """
    Column is a dictionary of cell: rowIndex -> cell
    """

    def __init__(self, colIndex: int, cellDict: dict):
        if type(cellDict) is dict:
            self.__cellDict = cellDict
            self.__colIndex = colIndex
            self.__rangeAddress = RangeAddress(CellIndex(self.__colIndex, 1),
                                               CellIndex(self.__colIndex, Column.elementLimit))
        else:
            raise ValueError("cellDict must be a dict")

    @staticmethod
    def empty(colIndex: int):
        """ create an empty Column """
        return ColumnImp(colIndex, {})


    ### >> Column << ###


    @property
    def index(self) -> int:
        return self.__colIndex

    def range(self, firstRow: int, lastRow: int) -> Range:
        """
        create a range from firstRow to lastRow
        :return: a range
        """
        firstCellAddress = CellIndex(self.index, firstRow)
        lastCellAddress = CellIndex(self.index, lastRow)
        return RangeImp(firstCellAddress, lastCellAddress, self)


    ### >> MutableCellContainer << ###


    def addCell(self, cell: Cell):
        if cell.address.colIndex == self.__colIndex:
            self.__cellDict[cell.address.rowIndex] = cell
        else:
            # can't add cell with col index that does not match this Column's col index
            raise ValueError("cell is in col {wrcol}, can't be inserted into col {ccol} "
                             .format(ccol=self.__colIndex, wrcol=cell.address.colIndex))

    def removeCell(self, address: CellAddress):
        del self.__cellDict[address.rowIndex]


    ### >> CellContainer << ###


    def hasCellAt(self, address: CellAddress):
        rowIsMatched = address.rowIndex in self.__cellDict.keys()
        colIsMatched = address.colIndex == self.__colIndex
        return colIsMatched and rowIsMatched

    def getCell(self, address: CellAddress) -> Cell:
        """
        :param address: cell position
        :return: either the cell at the input position or a TempCell with the same position if there aren't any cell at that position
        """
        if self.hasCellAt(address):
            return self.__cellDict[address.rowIndex]
        else:
            return TempCell(self, address)

    def isEmpty(self):
        return not bool(self.__cellDict)

    def containsAddress(self, cellAddress: CellAddress):
        return cellAddress.colIndex == self.__colIndex and cellAddress.rowIndex <= Column.elementLimit

    @property
    def cells(self) -> List[Cell]:
        return list(self.__cellDict.values())

    @property
    def rangeAddress(self) -> RangeAddress:
        return self.__rangeAddress


    ### >> Range << ###


    @property
    def firstCellAddress(self) -> CellAddress:
        return CellIndex(self.index,1)

    @property
    def lastCellAddress(self) -> CellAddress:
        return CellIndex(self.index,Column.elementLimit)


