from functools import partial
from typing import Optional, Union, Tuple, Callable

from bicp_document_structure.cell.Cell import Cell
from bicp_document_structure.cell.DataCell import DataCell
from bicp_document_structure.cell.WriteBackCell import WriteBackCell
from bicp_document_structure.cell.address.CellAddress import CellAddress
from bicp_document_structure.cell.address.CellIndex import CellIndex
from bicp_document_structure.formula_translator.FormulaTranslator import FormulaTranslator
from bicp_document_structure.range.Range import Range
from bicp_document_structure.range.Ranges import Ranges
from bicp_document_structure.range.address.RangeAddress import RangeAddress
from bicp_document_structure.range.address.RangeAddressImp import RangeAddressImp
from bicp_document_structure.util.AddressParser import AddressParser
from bicp_document_structure.util.Util import typeCheck
from bicp_document_structure.worksheet.Worksheet import Worksheet
from bicp_document_structure.worksheet.WorksheetConst import WorksheetConst
from bicp_document_structure.worksheet.WorksheetJson import WorksheetJson


class WorksheetImp(Worksheet):
    def __init__(self,
                 translatorGetter: Callable[[str], FormulaTranslator],
                 name = "",

                 ):
        # key = col index
        self._colDict: dict[int, list[Cell]] = {}
        # key = row index
        self._rowDict: dict[int, list[Cell]] = {}
        # key = (col, row)
        self._cellDict: dict[(int, int), Cell] = {}
        self.__name = name
        # self.__onCellChangeOfWorksheet:Optional[Callable[[Worksheet, Cell, P6Event], None]] = onCellChange
        self.translatorGetter: Callable[[str], FormulaTranslator] = translatorGetter

    ### >> ToJson << ###
    def toJsonDict(self) -> dict:
        return self.toJson().toJsonDict()

    @property
    def size(self) -> int:
        return len(self._cellDict)

    ### >> Worksheet << ###

    @property
    def translator(self) -> FormulaTranslator | None:
        return self.translatorGetter(self.name)

    @property
    def name(self) -> str:
        return self.__name

    def rename(self, newName: str):
        self.__name = newName

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
                    cell = DataCell(address, translatorGetter = partial(self.translatorGetter,self.name)),
                    container = self,
                )
            else:
                raise ValueError(f"worksheet \'{self.name}\' cannot not contain cell at address {address.__str__()}")
        else:
            return rt

    def addCell(self, cell: Cell):
        if self.containsAddress(cell.address):
            key = cell.address.toTuple()
            self._cellDict[key] = cell

            colIndex = cell.address.colIndex
            col = self._colDict.get(colIndex,[])
            col.append(cell)
            self._colDict[colIndex] = col

            rowIndex = cell.address.rowIndex
            row = self._rowDict.get(rowIndex,[])
            row.append(cell)
            self._rowDict[rowIndex] = row
        else:
            raise Exception(f"worksheet \'{self.name}\' can't contain cell at \'{cell.address.__str__()}\'")
    def removeCell(self, address: CellAddress):
        key = address.toTuple()
        (colIndex,rowIndex) = key
        if key in self._cellDict.keys():
            self._cellDict.pop(key)
        self._removeCellFromDict(self._colDict,colIndex,address)
        self._removeCellFromDict(self._rowDict,rowIndex,address)

    @staticmethod
    def _removeCellFromDict(targetDict, itemIndex:int, address:CellAddress):
        cellList = targetDict.get(itemIndex)
        if cellList is not None:
            cellList = list(filter(lambda cell: cell.address != address, cellList))
            if len(cellList) != 0:
                targetDict[itemIndex] = cellList
            else:
                targetDict.pop(itemIndex)




