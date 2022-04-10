from typing import Optional, Union, Tuple, Callable

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
from com.emeraldblast.p6.document_structure.worksheet.WorksheetConst import WorksheetConst
from com.emeraldblast.p6.document_structure.worksheet.WorksheetErrors import WorksheetErrors
from com.emeraldblast.p6.document_structure.worksheet.WorksheetJson import WorksheetJson


class WorksheetImp(Worksheet):

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
        return self._cellDict.get(address.toTuple()) is not None

    def containsAddress(self, address: CellAddress) -> bool:
        return self.rangeAddress.containCellAddress(address)

    @property
    def cells(self) -> list[Cell]:
        return list(self._cellDict.values())

    @property
    def rangeAddress(self) -> RangeAddressImp:
        return RangeAddressImp(
            CellIndex(1, 1),
            CellIndex(WorksheetConst.colLimit, WorksheetConst.rowLimit)
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
        else:
            raise Exception(f"worksheet \'{self.name}\' can't contain cell at \'{cell.address.__str__()}\'")

    def deleteCellRs(self, address: CellAddress | Tuple[int, int]|str) -> Result[None, ErrorReport]:
        address = CellAddresses.parseAddress(address)
        if self.containsAddress(address):
            key = address.toTuple()
            if key in self._cellDict.keys():
                self._cellDict.pop(key)
            (colIndex, rowIndex) = key
            self._removeCellFromDict(self._colDict, colIndex, address)
            self._removeCellFromDict(self._rowDict, rowIndex, address)
            return Ok(None)
        else:
            return Err(RangeErrors.CellNotInRangeReport(address, self.rangeAddress))


    @staticmethod
    def _removeCellFromDict(targetDict, itemIndex: int, address: CellAddress):
        cellList = targetDict.get(itemIndex)
        if cellList is not None:
            cellList = list(filter(lambda cell: cell.address != address, cellList))
            if len(cellList) != 0:
                targetDict[itemIndex] = cellList
            else:
                targetDict.pop(itemIndex)
