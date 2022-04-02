from functools import partial
from typing import Callable, Tuple, Optional

from bicp_document_structure.cell.Cell import Cell
from bicp_document_structure.cell.EventCell import EventCell
from bicp_document_structure.cell.address.CellAddress import CellAddress
from bicp_document_structure.communication.event.P6Events import P6Events
from bicp_document_structure.communication.internal_reactor.eventData.CellEventData import CellEventData
from bicp_document_structure.communication.internal_reactor.eventData.RangeEventData import RangeEventData
from bicp_document_structure.communication.internal_reactor.eventData.WorksheetEventData import WorksheetEventData
from bicp_document_structure.range.EventRange import EventRange
from bicp_document_structure.range.Range import Range
from bicp_document_structure.range.address.RangeAddress import RangeAddress
from bicp_document_structure.util.AddressParser import AddressParser
from bicp_document_structure.worksheet.Worksheet import Worksheet
from bicp_document_structure.worksheet.WorksheetWrapper import WorksheetWrapper


class EventWorksheet(WorksheetWrapper):
    def __init__(self,
                 innerWorksheet: Worksheet,
                 onCellEvent: Callable[[CellEventData], None] = None,
                 onWorksheetEvent: Callable[[WorksheetEventData], None] = None,
                 onRangeEvent: Callable[[RangeEventData], None] = None,
                 ):
        super().__init__(innerWorksheet)
        self.__onCellEvent: Callable[[CellEventData], None] = onCellEvent
        self.__onWorksheetEvent: Callable[[WorksheetEventData], None] = onWorksheetEvent
        self.__onRangeEvent: Callable[[RangeEventData], None] = onRangeEvent

    def __makePartial(self, callback):
        """create a partial function from a function by setting the 1st arg = self._innerSheet"""
        if callback is not None:
            return partial(callback, self._innerSheet)
        else:
            return None

    def getOrMakeCell(self, address: CellAddress) -> Cell:
        c: Cell = self._innerSheet.getOrMakeCell(address)
        return self._makeEventCell(c)

    def cell(self, address: str | CellAddress | Tuple[int, int]) -> Cell:
        parsedAddress = AddressParser.parseCellAddress(address)
        return self.getOrMakeCell(parsedAddress)

    def getCell(self, address: CellAddress) -> Optional[Cell]:
        cell = self._innerSheet.getCell(address)
        if cell is not None:
            return self._makeEventCell(cell)
        else:
            return cell

    def reRun(self):
        self._innerSheet.reRun()
        if self.__onWorksheetEvent is not None:
            # incomplete data
            eventData = WorksheetEventData(
                worksheet = self._innerSheet,
                event = P6Events.Worksheet.ReRun,
            )
            self.__onWorksheetEvent(eventData)

    def _XonCellEvent(self, data: CellEventData):
        data.worksheet = self._innerSheet
        if self.__onCellEvent is not None:
            self.__onCellEvent(data)

    def range(self, rangeAddress: str | RangeAddress | Tuple[CellAddress, CellAddress]) -> Range:
        rng = self._innerSheet.range(rangeAddress)

        def onRangeEvent(data: RangeEventData):
            data.worksheet = self._innerSheet
            if self.__onRangeEvent is not None:
                self.__onRangeEvent(data)

        evRange = EventRange(
            innerRange = rng,
            onCellEvent = self._XonCellEvent,
            onRangeEvent = onRangeEvent)
        return evRange

    @property
    def cells(self) -> list[Cell]:
        cs = self._innerSheet.cells
        rt = list(map(lambda c: self._makeEventCell(c), cs))
        return rt

    def _makeEventCell(self, cell: Cell) -> Cell:
        return EventCell(cell, onCellEvent = self._XonCellEvent)
