from typing import Callable, Optional, Union, Tuple

from bicp_document_structure.cell.Cell import Cell
from bicp_document_structure.cell.EventCell import EventCell
from bicp_document_structure.cell.address.CellAddress import CellAddress
from bicp_document_structure.communication.event.P6Event import P6Event
from bicp_document_structure.communication.event.P6Events import P6Events
from bicp_document_structure.range.Range import Range
from bicp_document_structure.range.RangeWrapper import RangeWrapper


class EventRange(RangeWrapper):

    def __init__(self, innerRange: Range,
                 onCellEvent: Callable[[Cell, P6Event], None] = None,
                 onRangeEvent: Callable[[Range, P6Event], None] = None,
                 ):
        super().__init__(innerRange)
        self.__onCellEvent = onCellEvent
        self.__onRangeEvent = onRangeEvent

    def __wrap(self, cell: Cell) -> Cell:
        return EventCell(cell, self.__onCellEvent)

    def cell(self, address: Union[str, CellAddress, Tuple[int, int]]) -> Cell:
        c = self._innerRange.cell(address)
        return self.__wrap(c)

    def getOrMakeCell(self, address: CellAddress) -> Cell:
        c = self._innerRange.getOrMakeCell(address)
        return self.__wrap(c)

    def getCell(self, address: CellAddress) -> Optional[Cell]:
        c = self._innerRange.getCell(address)
        if c is not None:
            return self.__wrap(c)
        else:
            return c

    @property
    def cells(self) -> list[Cell]:
        cs = self._innerRange.cells
        rt = list(map(lambda c: self.__wrap(c),cs))
        return rt

    def reRun(self):
        self._innerRange.reRun()
        if self.__onRangeEvent is not None:
            self.__onRangeEvent(self._innerRange,P6Events.Range.ReRun)
