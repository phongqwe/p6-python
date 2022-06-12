from typing import Optional, Union, Tuple, Callable

import pandas
import pyperclip
from com.emeraldblast.p6.document_structure.copy_paste.CopyErrors import CopyErrors

from com.emeraldblast.p6.document_structure.cell.util.CellUtils import CellUtils
from com.emeraldblast.p6.document_structure.communication.event.data_structure.range_event.RangeCopy import RangeCopy
from com.emeraldblast.p6.document_structure.copy_paste.Paster import Paster
from com.emeraldblast.p6.document_structure.copy_paste.Pasters import Pasters
from com.emeraldblast.p6.document_structure.util.CommonError import CommonErrors
from com.emeraldblast.p6.document_structure.worksheet.BaseWorksheet import BaseWorksheet

from com.emeraldblast.p6.proto.RangeProtos_pb2 import RangeCopyProto
from pandas import DataFrame

from com.emeraldblast.p6.document_structure.app.R import R
from com.emeraldblast.p6.document_structure.cell.Cell import Cell
from com.emeraldblast.p6.document_structure.cell.DataCell import DataCell
from com.emeraldblast.p6.document_structure.cell.WriteBackCell import WriteBackCell
from com.emeraldblast.p6.document_structure.cell.address.CellAddress import CellAddress
from com.emeraldblast.p6.document_structure.cell.address.CellAddresses import CellAddresses
from com.emeraldblast.p6.document_structure.cell.address.CellIndex import CellIndex
from com.emeraldblast.p6.document_structure.formula_translator.FormulaTranslator import FormulaTranslator
from com.emeraldblast.p6.document_structure.range.Range import Range
from com.emeraldblast.p6.document_structure.range.RangeErrors import RangeErrors
from com.emeraldblast.p6.document_structure.range.Ranges import Ranges
from com.emeraldblast.p6.document_structure.range.address.RangeAddress import RangeAddress
from com.emeraldblast.p6.document_structure.range.address.RangeAddressImp import RangeAddressImp
from com.emeraldblast.p6.document_structure.util.AddressParser import AddressParser
from com.emeraldblast.p6.document_structure.util.Util import typeCheck
from com.emeraldblast.p6.document_structure.util.report.error.ErrorReport import ErrorReport
from com.emeraldblast.p6.document_structure.util.result.Err import Err
from com.emeraldblast.p6.document_structure.util.result.Ok import Ok
from com.emeraldblast.p6.document_structure.util.result.Result import Result
from com.emeraldblast.p6.document_structure.workbook.WorkBook import Workbook
from com.emeraldblast.p6.document_structure.workbook.WorkbookErrors import WorkbookErrors
from com.emeraldblast.p6.document_structure.worksheet.Worksheet import Worksheet
from com.emeraldblast.p6.document_structure.worksheet.WorksheetErrors import WorksheetErrors
from com.emeraldblast.p6.document_structure.worksheet.WorksheetJson import WorksheetJson


class WorksheetImp(BaseWorksheet):

    @property
    def maxUsedCol(self) -> int | None:
        return self._maxCol

    @property
    def minUsedCol(self) -> int | None:
        return self._minCol

    @property
    def maxUsedRow(self) -> int | None:
        return self._maxRow

    @property
    def minUsedRow(self) -> int | None:
        return self._minRow

    @property
    def colDict(self) -> dict[int, list[Cell]]:
        return self._colDict

    @property
    def rowDict(self) -> dict[int, list[Cell]]:
        return self._rowDict

    def __init__(self,
                 name,
                 workbook: Workbook,
                 ):
        # key = col index
        self._colDict: dict[int, list[Cell]] = {}
        # key = row index
        self._rowDict: dict[int, list[Cell]] = {}
        # key = (col, row)
        self._cellDict: dict[(int, int), Cell] = {}
        self.__name = name

        def getTranslator(sheetName: str) -> FormulaTranslator:
            return self.workbook.getTranslator(sheetName)

        self.translatorGetter: Callable[[str], FormulaTranslator] = getTranslator
        self.__wb = workbook
        self._minCol = None
        self._maxCol = None
        self._minRow = None
        self._maxRow = None
        self._updateExtremeColRow()

    def _updateExtremeColRow(self):
        if not self.isEmpty():
            cols = self._colDict.keys()
            rows = self._rowDict.keys()
            if not self._colDict.get(self._minCol):
                self._minCol = min(cols)
            if not self._colDict.get(self._maxCol):
                self._maxCol = max(cols)
            if not self._rowDict.get(self._minRow):
                self._minRow = min(rows)
            if not self._rowDict.get(self._maxRow):
                self._maxRow = max(rows)

        else:
            self._minCol = None
            self._maxCol = None
            self._minRow = None
            self._maxRow = None

    def pasteDataFrameFromClipboardRs(self, anchorCell: CellAddress) -> Result[None, ErrorReport]:
        """
        paste a data frame or csv or excel-like data from clipboard into this worksheet
        :param anchorCell:
        :return: Ok if successfuly paste, Err otherwise
        """
        data = pandas.read_clipboard(header = None)
        if isinstance(data, DataFrame):
            df = data
            for rowIndex in range(len(df)):
                row = df.iloc[rowIndex]
                for colIndex in range(len(row)):
                    content = df.iloc[rowIndex, colIndex]
                    if not pandas.isna(content):
                        cell = self.cell((colIndex + anchorCell.colIndex , rowIndex + anchorCell.rowIndex ))
                        contentStr = str(content)
                        isFormula = contentStr.strip().startswith("=")
                        if isFormula:
                            cell.formula = content
                        else:
                            parsedValue = CellUtils.parseValue(content)
                            cell.value = parsedValue
            self.reRun()
            return Ok(None)
        else:
            return Err(CopyErrors.UnableToPasteRange.report())

    def pasteProtoFromClipboardRs(self, anchorCell: CellAddress, paster: Paster | None = None) -> Result[
        None, ErrorReport]:
        """paste a proto byte array from clipboard into this worksheet"""
        if paster is None:
            paster = Pasters.protoPaster
        rangCopyRs: Result[RangeCopy, ErrorReport] = paster.pasteRange()
        if rangCopyRs.isOk():
            rangeCopy = rangCopyRs.value
            originalTopLeft = rangeCopy.rangeId.rangeAddress.topLeft
            for copyCell in rangeCopy.cells:
                colDif = copyCell.col - originalTopLeft.colIndex
                rowDif = copyCell.row - originalTopLeft.rowIndex
                destinationCell = self.cell(CellAddresses.fromColRow(
                    col = anchorCell.colIndex + colDif,
                    row = anchorCell.rowIndex + rowDif
                ))
                destinationCell.copyFrom(copyCell)
            self.reRun()
            return Ok(None)
        else:
            return Err(CopyErrors.UnableToPasteRange.report())

    def deleteRangeRs(self, rangeAddress: RangeAddress) -> Result[None, ErrorReport]:
        tobeRemovedCells = []
        for cell in self.cells:
            address = cell.address
            if rangeAddress.containCellAddress(address):
                tobeRemovedCells.append(address)

        for address in tobeRemovedCells:
            self._cellDict.pop(address.toTuple())
            (colIndex, rowIndex) = address.toTuple()
            self._removeCellFromDict(self._colDict, colIndex, address)
            self._removeCellFromDict(self._rowDict, rowIndex, address)

        self._updateExtremeColRow()

        return Ok(None)

    def toJsonDict(self) -> dict:
        return self.toJson().toJsonDict()

    @property
    def size(self) -> int:
        return len(self._cellDict)

    @property
    def rootWorksheet(self) -> 'Worksheet':
        return self

    @property
    def workbook(self) -> Workbook | None:
        return self.__wb

    @workbook.setter
    def workbook(self, newWorkbook: Workbook | None):
        if newWorkbook is not None:
            self.__wb = newWorkbook.rootWorkbook
        else:
            self.__wb = newWorkbook

    @property
    def translator(self) -> FormulaTranslator | None:
        return self.translatorGetter(self.name)

    @property
    def name(self) -> str:
        return self.__name

    def internalRename(self, newName: str):
        self.__name = newName

    def renameRs(self, newSheetName: str) -> Result[None, ErrorReport]:
        if len(newSheetName) == 0 or newSheetName is None:
            return Err(WorksheetErrors.IllegalNameReport(newSheetName))

        if self.name == newSheetName:
            return Ok(None)

        newNameOk = self.workbook.getWorksheetOrNone(newSheetName) is None

        if newNameOk:
            oldName = self.name
            self.__name = newSheetName
            # update sheet dict
            # cache workbook in a var because removeWorksheet will nullify self.workbook
            wb = self.workbook
            wb.updateSheetName(oldName, self)
            return Ok(None)
        else:
            return Err(WorkbookErrors.WorksheetAlreadyExistReport(newSheetName))

    def toJson(self) -> WorksheetJson:
        cellJsons = []
        for cell in self.cells:
            cellJsons.append(cell.toJson())
        return WorksheetJson(self.__name, cellJsons)

    ### >> UserFriendlyCellContainer << ##
    def cell(self, address: Union[str, CellAddress, Tuple[int, int]]) -> Cell:
        parsedAddress: CellAddress = AddressParser.parseCellAddress(address)
        return self.getOrMakeCell(parsedAddress)

    ### >> UserFriendlyWorksheet << ###

    def range(self, rangeAddress: Union[str, RangeAddress, Tuple[CellAddress, CellAddress]]) -> Range:
        parsedAddress = AddressParser.parseRangeAddress(rangeAddress)
        return Ranges.fromRangeAddress(parsedAddress, self)

    ### >> CellContainer << ###

    def isSameRangeAddress(self, other):
        """
        :raise ValueError of other is not a Worksheet
        :param other: other Worksheet
        :return: always return True because every worksheet has the same fixed range address
        """
        typeCheck(other, "other", Worksheet)
        return self.rangeAddress == other.rangeAddress

    def getCell(self, address: CellAddress) -> Optional[Cell]:
        return self._cellDict.get(address.toTuple())

    def hasCellAt(self, address: CellAddress) -> bool:
        typeCheck(address, "address", CellAddress)
        return self.hasCellAtIndex(address.colIndex, address.rowIndex)

    def containsAddress(self, address: CellAddress) -> bool:
        return self.rangeAddress.containCellAddress(address)

    def containsAddressIndex(self, col: int, row: int) -> bool:
        return self.rangeAddress.containColRow(col, row)

    def hasCellAtIndex(self, col: int, row: int) -> bool:
        return self._cellDict.get((col, row)) is not None

    @property
    def cells(self) -> list[Cell]:
        return list(self._cellDict.values())

    @property
    def rangeAddress(self) -> RangeAddressImp:
        return RangeAddressImp(
            CellIndex(1, 1),
            CellIndex(R.WorksheetConsts.colLimit, R.WorksheetConsts.rowLimit)
        )

    ### >> MutableCellContainer << ###

    def getOrMakeCell(self, address: CellAddress) -> Cell:
        key = (address.colIndex, address.rowIndex)
        rt: Cell | None = self._cellDict.get(key)
        if rt is None:
            if self.containsAddress(address):
                return WriteBackCell(
                    cell = DataCell(address,
                                    worksheet = self),
                    container = self,
                )
            else:
                raise ValueError(f"worksheet \'{self.name}\' cannot not contain cell at address {address.__str__()}")
        else:
            return rt

    def addCell(self, cell: Cell):
        if self.containsAddress(cell.address):
            # add cell to cell dict
            key = cell.address.toTuple()
            self._cellDict[key] = cell

            # add cell to col dict
            colIndex = cell.address.colIndex
            col = self._colDict.get(colIndex, [])
            col.append(cell)
            self._colDict[colIndex] = col

            # add cell row dict
            rowIndex = cell.address.rowIndex
            row = self._rowDict.get(rowIndex, [])
            row.append(cell)
            self._rowDict[rowIndex] = row

            # update cell reference
            cell.worksheet = self

            # update extremities
            if (self._maxCol is not None and cell.col > self._maxCol) or self._maxCol is None:
                self._maxCol = cell.col
            if (self._minCol is not None and cell.col < self._minCol) or self._minCol is None:
                self._minCol = cell.col
            if (self._maxRow is not None and cell.row > self._maxRow) or self._maxRow is None:
                self._maxRow = cell.row
            if (self._minRow is not None and cell.row < self._minRow) or self._minRow is None:
                self._minRow = cell.row
        else:
            raise Exception(f"worksheet \'{self.name}\' can't contain cell at \'{cell.address.__str__()}\'")

    def deleteCellRs(self, address: CellAddress | Tuple[int, int] | str) -> Result[None, ErrorReport]:
        address: CellAddress = CellAddresses.parseAddress(address)
        if self.containsAddress(address):
            key = address.toTuple()
            if key in self._cellDict.keys():
                self._cellDict.pop(key)
            (colIndex, rowIndex) = key
            self._removeCellFromDict(self._colDict, colIndex, address)
            self._removeCellFromDict(self._rowDict, rowIndex, address)

            # update extremities
            self._updateExtremeColRow()
            return Ok(None)
        else:
            return Err(RangeErrors.CellNotInRangeReport.report(address, self.rangeAddress))

    @staticmethod
    def _removeCellFromDict(targetDict, itemIndex: int, address: CellAddress):
        cellList = targetDict.get(itemIndex)
        if cellList is not None:
            cellList = list(filter(lambda cell: cell.address != address, cellList))
            if len(cellList) != 0:
                targetDict[itemIndex] = cellList
            else:
                targetDict.pop(itemIndex)
