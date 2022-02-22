from functools import partial
from typing import Callable, Tuple, Optional

from bicp_document_structure.cell.Cell import Cell
from bicp_document_structure.cell.EventCell import EventCell
from bicp_document_structure.cell.address.CellAddress import CellAddress
from bicp_document_structure.column.Column import Column
from bicp_document_structure.column.EventColumn import EventColumn
from bicp_document_structure.event.P6Event import P6Event
from bicp_document_structure.event.P6Events import P6Events
from bicp_document_structure.range.EventRange import EventRange
from bicp_document_structure.range.Range import Range
from bicp_document_structure.range.address.RangeAddress import RangeAddress
from bicp_document_structure.util.AddressParser import AddressParser
from bicp_document_structure.worksheet.Worksheet import Worksheet
from bicp_document_structure.worksheet.WorksheetWrapper import WorksheetWrapper


class EventWorksheet(WorksheetWrapper):
    def __init__(self,
                 innerWorksheet: Worksheet,
                 onCellChange: Callable[[Worksheet, Cell, P6Event], None] = None,
                 onWorksheetEvent: Callable[[Worksheet, P6Event], None] = None,
                 onRangeEvent: Callable[[Worksheet, Range, P6Event], None] = None,
                 onColEvent: Callable[[Worksheet, Column, P6Event], None] = None,
                 ):
        super().__init__(innerWorksheet)
        self.__onCellEvent: Callable[[Worksheet, Cell, P6Event], None] = onCellChange
        self.__onWorksheetEvent: Callable[[Worksheet, P6Event], None] = onWorksheetEvent
        self.__onRangeEvent: Callable[[Worksheet, Range, P6Event], None] = onRangeEvent
        self.__onColEvent: Callable[[Worksheet, Column, P6Event], None] = onColEvent

    def __makePartial(self, callback):
        """create a partial function from a function by setting the 1st arg = self._innerSheet"""
        if callback is not None:
            return partial(callback, self._innerSheet)
        else:
            return None

    def getCol(self, colIndex: int) -> Column:
        innerCol = self._innerSheet.getCol(colIndex)
        return EventColumn(innerCol,
                           onCellChange = self.__makePartial(self.__onCellEvent),
                           onRangeEvent = self.__makePartial(self.__onRangeEvent),
                           onColEvent = self.__makePartial(self.__onColEvent),
                           )

    def getOrMakeCell(self, address: CellAddress) -> Cell:
        col = self.getCol(address.colIndex)
        rt = col.getOrMakeCell(address)
        return rt

    def cell(self, address: str | CellAddress | Tuple[int, int]) -> Cell:
        parsedAddress = AddressParser.parseCellAddress(address)
        return self.getOrMakeCell(parsedAddress)

    def getCell(self, address: CellAddress) -> Optional[Cell]:
        cell = self._innerSheet.getCell(address)
        if cell is not None:
            return self.__wrap(cell)
        else:
            return cell

    def reRun(self):
        self._innerSheet.reRun()
        if self.__onWorksheetEvent is not None:
            self.__onWorksheetEvent(self._innerSheet, P6Events.Worksheet.ReRun)

    def range(self, rangeAddress: str | RangeAddress | Tuple[CellAddress, CellAddress]) -> Range:
        rng = self._innerSheet.range(rangeAddress)
        evRange = EventRange(rng,
                             onCellEvent = self.__makePartial(self.__onCellEvent),
                             onRangeEvent = self.__makePartial(self.__onRangeEvent),
                             )
        return evRange

    @property
    def cells(self) -> list[Cell]:
        cs = self._innerSheet.cells
        rt = list(map(lambda c: self.__wrap(c), cs))
        return rt

    def __wrap(self, cell: Cell) -> Cell:
        return EventCell(cell, onCellEvent = self.__makePartial(self.__onCellEvent))