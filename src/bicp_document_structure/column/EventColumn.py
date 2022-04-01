from typing import Callable, Optional, Union, Tuple

from bicp_document_structure.cell.Cell import Cell
from bicp_document_structure.cell.EventCell import EventCell
from bicp_document_structure.cell.address.CellAddress import CellAddress
from bicp_document_structure.column.Column import Column
from bicp_document_structure.column.ColumnWrapper import ColumnWrapper
from bicp_document_structure.communication.event.P6Event import P6Event
from bicp_document_structure.communication.event.P6Events import P6Events
from bicp_document_structure.range.EventRange import EventRange
from bicp_document_structure.range.Range import Range


class EventColumn(ColumnWrapper):
    def __init__(self, innerCol: Column,
                 onCellChange: Callable[[Cell, P6Event], None] = None,
                 onRangeEvent: Callable[[Range, P6Event], None] = None,
                 onColEvent: Callable[[Column, P6Event], None] = None,
                 ):
        super().__init__(innerCol)
        self.__onCellEvent = onCellChange
        self.__onRangeEvent = onRangeEvent
        self.__onColEvent = onColEvent

    def getOrMakeCell(self, address: CellAddress) -> Cell:
        """
        :param address: cell position
        :return: a WriteBackCell
        """
        cell = self._innerCol.getOrMakeCell(address)
        rt = self.__wrapCellInEventCell(cell)
        return rt

    def range(self, firstRow: int, lastRow: int) -> Range:
        rng = self._innerCol.range(firstRow, lastRow)
        rt = EventRange(
            rng,
            onCellEvent = self.__onCellEvent,
            onRangeEvent = self.__onRangeEvent,
        )
        return rt

    def cell(self, address: Union[str, CellAddress, Tuple[int, int]]) -> Cell:
        c = self._innerCol.cell(address)
        ec = self.__wrapCellInEventCell(c)
        return ec

    def __wrapCellInEventCell(self, cell: Cell) -> Cell:
        return EventCell(cell, self.__onCellEvent)

    def getCell(self, address: CellAddress) -> Optional[Cell]:
        c = self._innerCol.getCell(address)
        if c is not None:
            return self.__wrapCellInEventCell(c)
        else:
            return c

    @property
    def cells(self) -> list[Cell]:
        cs = self._innerCol.cells
        ecs = list(map(lambda c: self.__wrapCellInEventCell(c), cs))
        return ecs

    def reRun(self):
        self._innerCol.reRun()
        if self.__onColEvent is not None:
            self.__onColEvent(self._innerCol, P6Events.Column.ReRun)
