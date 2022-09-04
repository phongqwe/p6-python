from typing import Callable, Optional, Union, Tuple

from com.qxdzbc.p6.document_structure.cell.Cell import Cell
from com.qxdzbc.p6.document_structure.cell.EventCell import EventCell
from com.qxdzbc.p6.document_structure.cell.address.CellAddress import CellAddress
from com.qxdzbc.p6.document_structure.communication.event.data_structure.common.ErrorIndicator import \
    ErrorIndicator
from com.qxdzbc.p6.document_structure.communication.event.data_structure.range_event.RangeId import RangeId
from com.qxdzbc.p6.document_structure.communication.event.data_structure.range_event.range_to_clipboard.RangeToClipboardResponse import \
    RangeToClipboardResponse
from com.qxdzbc.p6.document_structure.communication.notifier.eventData.EventData import EventData
from com.qxdzbc.p6.document_structure.range.Range import Range
from com.qxdzbc.p6.document_structure.range.RangeWrapper import RangeWrapper
from com.qxdzbc.p6.document_structure.util.report.error.ErrorReport import ErrorReport
from com.qxdzbc.p6.document_structure.util.result.Result import Result


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
        c = self.rootRange.cell(address)
        return self.__makeEventCell(c)

    def getOrMakeCell(self, address: CellAddress) -> Cell:
        c = self.rootRange.getOrMakeCell(address)
        return self.__makeEventCell(c)

    def getCell(self, address: CellAddress) -> Optional[Cell]:
        c = self.rootRange.getCell(address)
        if c is not None:
            return self.__makeEventCell(c)
        else:
            return c

    @property
    def cells(self) -> list[Cell]:
        cs = self.rootRange.cells
        rt = list(map(lambda c: self.__makeEventCell(c), cs))
        return rt

    # def reRun(self):
    #     self.rootRange.reRun()
    #     if self.__onRangeEvent is not None:
    #         data = EventData(
    #             event = P6Events.Range.ReRun.event,
    #             isError = False
    #         )
    #         self.__onRangeEvent(data)

    def copyValueDataFrame(self):
        self.rootRange.copyValueDataFrame()
        self.__emitCopyEvent(ErrorIndicator.noError())


    def copyToClipboardAsProto(self) -> Result[None, ErrorReport]:
        rs = self.rootRange.copyToClipboardAsProto()
        errorIndicator = ErrorIndicator.noError()
        if rs.isErr():
            errorIndicator = ErrorIndicator.error(rs.err)
        self.__emitCopyEvent(errorIndicator)
        return rs

    def __emitCopyEvent(self, errorIndicator):
        res = RangeToClipboardResponse(
            errorIndicator = errorIndicator,
            rangeId = RangeId(
                rangeAddress = self.rangeAddress,
                workbookKey = self.worksheet.workbook.workbookKey,
                worksheetName = self.worksheet.name
            ),
            windowId = None
        )

        # eventData = EventData(
        #     event = P6Events.Range.RangeToClipBoard.event,
        #     isError = False,
        #     data = res.toProtoBytes()
        # )
        self.__onRangeEvent(res.toEventData())
