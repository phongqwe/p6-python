from typing import List, Optional, Union, Tuple

from bicp_document_structure.cell.Cell import Cell
from bicp_document_structure.cell.DataCell import DataCell
from bicp_document_structure.cell.WriteBackCell import WriteBackCell
from bicp_document_structure.cell.address.CellAddress import CellAddress
from bicp_document_structure.cell.address.CellIndex import CellIndex
from bicp_document_structure.column.Column import Column
from bicp_document_structure.column.ColumnJson import ColumnJson
from bicp_document_structure.range.Range import Range
from bicp_document_structure.range.RangeImp import RangeImp
from bicp_document_structure.range.address.RangeAddressImp import RangeAddressImp
from bicp_document_structure.util.AddressParser import AddressParser
from bicp_document_structure.worksheet.WorksheetConst import WorksheetConst


class ColumnImp(Column):
    """
    Column is a dictionary of cell: rowIndex -> cell
    """

    def __init__(self, colIndex: int, cellDict: dict):
        if type(cellDict) is dict:
            self.__cellDict = cellDict
            self.__colIndex = colIndex
            self.__rangeAddress = RangeAddressImp(CellIndex(self.__colIndex, 1),
                                                  CellIndex(self.__colIndex, WorksheetConst.rowLimit))
        else:
            raise ValueError("cellDict must be a dict")

    @staticmethod
    def empty(colIndex: int):
        """ create an empty Column """
        return ColumnImp(colIndex, {})

    ### >> Column << ###

    def toJson(self) -> ColumnJson:
        return ColumnJson(
            colIndex=self.index,
            cells=self.cells
        )

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
        if self.containsAddress(cell.address):
            self.__cellDict[cell.address.rowIndex] = cell
        else:
            # can't add cell with col index that does not match this Column's col index
            raise ValueError("cell is in col {wrcol}, can't be inserted into col {ccol} "
                             .format(ccol=self.__colIndex, wrcol=cell.address.colIndex))

    def removeCell(self, address: CellAddress):
        del self.__cellDict[address.rowIndex]

    def getOrMakeCell(self, address: CellAddress) -> Cell:
        """
        :param address: cell position
        :return: a WriteBackCell
        """
        cell = self.getCell(address)
        if cell is not None:
            return cell
        if self.containsAddress(address):
            return WriteBackCell(DataCell(address),self)
        else:
            raise ValueError("colum {cl} does not contain {adr}".format(
                cl=str(self.index),
                adr=address.__str__()
            ))

    ### >> CellContainer << ###

    def hasCellAt(self, address: CellAddress):
        rowIsMatched = address.rowIndex in self.__cellDict.keys()
        colIsMatched = address.colIndex == self.__colIndex
        return colIsMatched and rowIsMatched

    def getCell(self, address: CellAddress) -> Optional[Cell]:
        if self.hasCellAt(address):
            return self.__cellDict[address.rowIndex]
        else:
            return None

    def isSameRangeAddress(self, other):
        return super().isSameRangeAddress(other)

    def isEmpty(self):
        return not bool(self.__cellDict)

    def containsAddress(self, cellAddress: CellAddress):
        colOk = cellAddress.colIndex == self.__colIndex
        rowOk = cellAddress.rowIndex <= WorksheetConst.rowLimit
        return colOk and rowOk

    @property
    def cells(self) -> List[Cell]:
        return list(self.__cellDict.values())

    @property
    def rangeAddress(self) -> RangeAddressImp:
        return self.__rangeAddress

    ### >> Range << ###

    @property
    def firstCellAddress(self) -> CellAddress:
        return CellIndex(self.index, 1)

    @property
    def lastCellAddress(self) -> CellAddress:
        return CellIndex(self.index, WorksheetConst.rowLimit)

    ### >> UserFriendlyCellContainer << ###

    def cell(self, address: Union[str, CellAddress, Tuple[int, int]]) -> Cell:
        parsedAddress = AddressParser.parseCellAddress(address)
        return self.getOrMakeCell(parsedAddress)
