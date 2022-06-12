from abc import ABC
from typing import Optional

from com.emeraldblast.p6.document_structure.app.R import R
from com.emeraldblast.p6.document_structure.cell.address.CellAddress import CellAddress
from com.emeraldblast.p6.document_structure.cell.address.CellAddresses import CellAddresses
from com.emeraldblast.p6.document_structure.util.AlphabetBaseNumberSystem import AlphabetBaseNumberSystem
from com.emeraldblast.p6.document_structure.util.ToProto import ToProto
from com.emeraldblast.p6.proto.DocProtos_pb2 import RangeAddressProto


class RangeAddress(ToProto[RangeAddressProto],ABC):
    """
    This interface represents a range address.
    Label format:
    first cell - last cell: "@A1:B3"
    whole column: "@A:D"
    whole row: "@22:33"
    """

    def intersect(self, otherRangeAddress: 'RangeAddress') -> Optional['RangeAddress'] :
        raise NotImplementedError()

    @property
    def label(self) -> str:
        firstCellOnFirstRow = self.topLeft.rowIndex == 1
        lastCellOnLastRow = self.botRight.rowIndex == R.WorksheetConsts.rowLimit
        if firstCellOnFirstRow and lastCellOnLastRow:
            firstColLabel = AlphabetBaseNumberSystem.fromDecimal(self.topLeft.colIndex)
            lastColLabel = AlphabetBaseNumberSystem.fromDecimal(self.botRight.colIndex)
            return "@{firstCol}:{lastCol}".format(
                firstCol=firstColLabel, lastCol=lastColLabel
            )

        firstCellOnFirstCol = self.topLeft.colIndex == 1
        lastCellOnLastCol = self.botRight.colIndex == R.WorksheetConsts.colLimit
        if firstCellOnFirstCol and lastCellOnLastCol:
            return "@{firstRow}:{lastRow}".format(
                firstRow=str(self.topLeft.rowIndex),
                lastRow=str(self.botRight.rowIndex)
            )

        firstCellLabel = self.topLeft.rawLabel
        lastCellLabel = self.botRight.rawLabel
        return "@{fa}:{la}".format(
            fa=firstCellLabel,
            la=lastCellLabel
        )


    def __str__(self) -> str:
        return "[{fc}:{lc}]".format(fc=str(self.topLeft), lc=str(self.botRight))
    @property
    def firstRowIndex(self) -> int:
        return self.topLeft.rowIndex

    @property
    def lastRowIndex(self) -> int:
        return self.botRight.rowIndex

    @property
    def firstColIndex(self) -> int:
        return self.topLeft.colIndex

    @property
    def lastColIndex(self) -> int:
        return self.botRight.colIndex

    def containCellAddress(self, cellAddress: CellAddress):
        return self.containColRow(cellAddress.colIndex,cellAddress.rowIndex)

    def containColRow(self,col:int, row:int):
        colOk = self.firstColIndex <= col <= self.lastColIndex
        rowOk = self.firstRowIndex <= row <= self.lastRowIndex
        return colOk and rowOk

    @property
    def topLeft(self) -> CellAddress:
        raise NotImplementedError()

    @property
    def botRight(self) -> CellAddress:
        raise NotImplementedError()

    def rowCount(self) -> int:
        raise NotImplementedError()

    def colCount(self) -> int:
        raise NotImplementedError()

    @property
    def topRight(self) -> CellAddress:
        return CellAddresses.fromColRow(self.lastColIndex, self.firstRowIndex)

    @property
    def botLeft(self) -> CellAddress:
        return CellAddresses.fromColRow(self.firstColIndex, self.lastRowIndex)

    def moveByTopLeftTo(self, newTopLeft:CellAddress) -> 'RangeAddress':
        """move this range so that its top left become the new provided top left. Consequently, this will also change the rest of the vertices
        :return a new range address
        """

        raise NotImplementedError()