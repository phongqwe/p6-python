from abc import ABC

from com.emeraldblast.p6.document_structure.cell.address.CellAddress import CellAddress
from com.emeraldblast.p6.document_structure.util.AlphabetBaseNumberSystem import AlphabetBaseNumberSystem
from com.emeraldblast.p6.document_structure.worksheet.WorksheetConst import WorksheetConst


class RangeAddress(ABC):

    @property
    def label(self) -> str:
        # TODO add code to simplify whole column/range to shorten address
        firstCellOnFirstRow = self.firstAddress.rowIndex == 1
        lastCellOnLastRow = self.lastAddress.rowIndex == WorksheetConst.rowLimit
        if firstCellOnFirstRow and lastCellOnLastRow:
            firstColLabel = AlphabetBaseNumberSystem.fromDecimal(self.firstAddress.colIndex)
            lastColLabel = AlphabetBaseNumberSystem.fromDecimal(self.lastAddress.colIndex)
            return "@{firstCol}:{lastCol}".format(
                firstCol=firstColLabel, lastCol=lastColLabel
            )

        firstCellOnFirstCol = self.firstAddress.colIndex == 1
        lastCellOnLastCol = self.lastAddress.colIndex == WorksheetConst.colLimit
        if firstCellOnFirstCol and lastCellOnLastCol:
            return "@{firstRow}:{lastRow}".format(
                firstRow=str(self.firstAddress.rowIndex),
                lastRow=str(self.lastAddress.rowIndex)
            )

        firstCellLabel = self.firstAddress.rawLabel
        lastCellLabel = self.lastAddress.rawLabel
        return "@{fa}:{la}".format(
            fa=firstCellLabel,
            la=lastCellLabel
        )

    def __str__(self) -> str:
        return self.label

    @property
    def firstRowIndex(self) -> int:
        return self.firstAddress.rowIndex

    @property
    def lastRowIndex(self) -> int:
        return self.lastAddress.rowIndex

    @property
    def firstColIndex(self) -> int:
        return self.firstAddress.colIndex

    @property
    def lastColIndex(self) -> int:
        return self.lastAddress.colIndex

    def containCellAddress(self, cellAddress: CellAddress):
        colOk = self.firstColIndex <= cellAddress.colIndex <= self.lastColIndex
        rowOk = self.firstRowIndex <= cellAddress.rowIndex <= self.lastRowIndex
        return colOk and rowOk

    @property
    def firstAddress(self) -> CellAddress:
        raise NotImplementedError()

    @property
    def lastAddress(self) -> CellAddress:
        raise NotImplementedError()

    def rowCount(self) -> int:
        raise NotImplementedError()

    def colCount(self) -> int:
        raise NotImplementedError()
