from typing import List, Union, Tuple, Optional, Callable

from bicp_document_structure.cell.Cell import Cell
from bicp_document_structure.cell.DataCell import DataCell
from bicp_document_structure.cell.WriteBackCell import WriteBackCell
from bicp_document_structure.cell.address.CellAddress import CellAddress
from bicp_document_structure.column.Column import Column
from bicp_document_structure.column.ColumnJson import ColumnJson
from bicp_document_structure.column.MutableColumnContainer import MutableColumnContainer
from bicp_document_structure.mutation.CellMutationEvent import CellMutationEvent
from bicp_document_structure.range.Range import Range
from bicp_document_structure.range.address.RangeAddressImp import RangeAddressImp


class WriteBackColumn(Column):


    def __init__(self, col:Column, container: MutableColumnContainer):
        self.__innerCol:Column = col
        self.__container = container
        self.__onCellMutation = self.__innerCol._onCellMutationEventHandler

    ### >> Column << ##

    @property
    def _onCellMutationEventHandler(self) -> Callable[[Cell, CellMutationEvent], None]:
        return self.__innerCol._onCellMutationEventHandler

    def range(self, firstRow: int, lastRow: int) -> Range:
        return self.__innerCol.range(firstRow, lastRow)

    @property
    def index(self) -> int:
        return self.__innerCol.index

    def toJson(self) -> ColumnJson:
        return self.__innerCol.toJson()

    ### >> Range << ###

    @property
    def firstCellAddress(self) -> CellAddress:
        return self.__innerCol.firstCellAddress

    @property
    def lastCellAddress(self) -> CellAddress:
        return self.__innerCol.lastCellAddress

    def containsAddress(self, address: CellAddress) -> bool:
        return self.__innerCol.containsAddress(address)

    @property
    def cells(self) -> List[Cell]:
        return self.__innerCol.cells

    ### >> CellContainer << ###

    def hasCellAt(self, address: CellAddress) -> bool:
        return self.__innerCol.hasCellAt(address)

    def getOrMakeCell(self, address: CellAddress) -> Cell:
        # rt= self.__innerCol.getOrMakeCell(address)
        # return rt
        if self.hasCellAt(address):
            return self.__innerCol.getOrMakeCell(address)
        else:
            return WriteBackCell(
                cell=DataCell(address,onCellMutation=self.__onCellMutation),
                container=self,
            )

    def isEmpty(self) -> bool:
        return self.__innerCol.isEmpty()

    @property
    def rangeAddress(self) -> RangeAddressImp:
        return self.__innerCol.rangeAddress

    ### >> CellContainer << ###

    def addCell(self, cell: Cell):
        self.__innerCol.addCell(cell)
        # write this temp col to the container when a new cell is added
        columnNotWritten = not self.__container.hasColumn(self.__innerCol.index)
        if columnNotWritten:
            self.__container.setCol(self.__innerCol)

    def removeCell(self, address: CellAddress):
        self.__innerCol.removeCell(address)

    def getCell(self, address: CellAddress) -> Optional[Cell]:
        return self.__innerCol.getCell(address)

    def isSameRangeAddress(self, other):
        return self.__innerCol.isSameRangeAddress(other)

    ### >> UserFriendCellContainer << ##
    def cell(self, address: Union[str, CellAddress, Tuple[int, int]]) -> Cell:
        return self.__innerCol.cell(address)

    def __eq__(self, o: object) -> bool:
        if isinstance(o,Column):
            return self.__innerCol == o
        else:
            return False