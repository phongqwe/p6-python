from typing import Callable, Optional, Union, Tuple

from com.emeraldblast.p6.document_structure.cell.Cell import Cell
from com.emeraldblast.p6.document_structure.cell.EventCell import EventCell
from com.emeraldblast.p6.document_structure.cell.address.CellAddress import CellAddress
from com.emeraldblast.p6.document_structure.communication.event.P6Events import P6Events
from com.emeraldblast.p6.document_structure.communication.notifier.eventData.AppEventData import EventData
from com.emeraldblast.p6.document_structure.range.Range import Range
from com.emeraldblast.p6.document_structure.range.RangeWrapper import RangeWrapper


class EventRange(RangeWrapper):

    def __init__(self, innerRange: Range,
                 onCellEvent: Callable[[EventData], None] = None,
                 onRangeEvent: Callable[[EventData], None] = None,
                 ):
        super().__init__(innerRange)
        self.__onCellEvent = onCellEvent
        self.__onRangeEvent = onRangeEvent

    def __makeEventCell(self, cell: Cell) -> Cell:
        return EventCell(cell, self.__onCellEvent)

    def cell(self, address: Union[str, CellAddress, Tuple[int, int]]) -> Cell:
        c = self._innerRange.cell(address)
        return self.__makeEventCell(c)

    def getOrMakeCell(self, address: CellAddress) -> Cell:
        c = self._innerRange.getOrMakeCell(address)
        return self.__makeEventCell(c)

    def getCell(self, address: CellAddress) -> Optional[Cell]:
        c = self._innerRange.getCell(address)
        if c is not None:
            return self.__makeEventCell(c)
        else:
            return c

    @property
    def cells(self) -> list[Cell]:
        cs = self._innerRange.cells
        rt = list(map(lambda c: self.__makeEventCell(c), cs))
        return rt

    def reRun(self):
        self._innerRange.reRun()
        if self.__onRangeEvent is not None:
            data = EventData(
                event = P6Events.Range.ReRun.event,
                isError = False
            )
            self.__onRangeEvent(data)
