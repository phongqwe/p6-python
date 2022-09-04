from functools import partial
from typing import Callable, Tuple, Optional

from com.qxdzbc.p6.document_structure.cell.Cell import Cell
from com.qxdzbc.p6.document_structure.cell.EventCell import EventCell
from com.qxdzbc.p6.document_structure.cell.address.CellAddress import CellAddress
from com.qxdzbc.p6.document_structure.cell.address.CellAddresses import CellAddresses
from com.qxdzbc.p6.document_structure.communication.event.data_structure.range_event.paste_range.PasteRangeResponse import \
    PasteRangeResponse
from com.qxdzbc.p6.document_structure.communication.event.data_structure.worksheet_event.DeleteCellResponse import \
    DeleteCellResponse
from com.qxdzbc.p6.document_structure.communication.event.data_structure.worksheet_event.DeleteMultiResponse import \
    DeleteMultiResponse
from com.qxdzbc.p6.document_structure.communication.event.data_structure.worksheet_event.RenameWorksheetResponse import \
    RenameWorksheetResponse
from com.qxdzbc.p6.document_structure.communication.notifier.eventData.EventData import EventData
from com.qxdzbc.p6.document_structure.copy_paste.paster.Paster import Paster
from com.qxdzbc.p6.document_structure.range.EventRange import EventRange
from com.qxdzbc.p6.document_structure.range.Range import Range
from com.qxdzbc.p6.document_structure.range.address.RangeAddress import RangeAddress
from com.qxdzbc.p6.document_structure.util.AddressParser import AddressParser
from com.qxdzbc.p6.document_structure.util.report.error.ErrorReport import ErrorReport
from com.qxdzbc.p6.document_structure.util.result.Result import Result
from com.qxdzbc.p6.document_structure.worksheet.Worksheet import Worksheet
from com.qxdzbc.p6.document_structure.worksheet.WorksheetWrapper import WorksheetWrapper


class EventWorksheet(WorksheetWrapper):
    def __init__(self,
                 innerWorksheet: Worksheet,
                 onCellEvent: Callable[[EventData], None] = None,
                 onWorksheetEvent: Callable[[EventData], None] = None,
                 onRangeEvent: Callable[[EventData], None] = None,
                 ):
        super().__init__(innerWorksheet)
        self.__onCellEvent: Callable[[EventData], None] = onCellEvent
        self.__onWorksheetEvent: Callable[[EventData], None] = onWorksheetEvent
        self.__onRangeEvent: Callable[[EventData], None] = onRangeEvent
        self._iws = innerWorksheet

    def __makePartial(self, callback):
        """create a partial function from a function by setting the 1st arg = self.rootWorksheet"""
        if callback is not None:
            return partial(callback, self.rootWorksheet)
        else:
            return None

    def getOrMakeCell(self, address: CellAddress) -> Cell:
        c: Cell = self.rootWorksheet.getOrMakeCell(address)
        return self._makeEventCell(c)

    def cell(self, address: str | CellAddress | Tuple[int, int]) -> Cell:
        parsedAddress = AddressParser.parseCellAddress(address)
        return self.getOrMakeCell(parsedAddress)

    def getCell(self, address: CellAddress) -> Optional[Cell]:
        cell = self.rootWorksheet.getCell(address)
        if cell is not None:
            return self._makeEventCell(cell)
        else:
            return cell

    def _onCellEvent(self, data: EventData):
        data.worksheet = self.rootWorksheet
        if self.__onCellEvent is not None:
            self.__onCellEvent(data)

    def range(self, rangeAddress: str | RangeAddress | Tuple[CellAddress, CellAddress]) -> Range:
        rng = self.rootWorksheet.range(rangeAddress)

        def onRangeEvent(data: EventData):
            if self.__onRangeEvent is not None:
                self.__onRangeEvent(data)

        evRange = EventRange(
            innerRange = rng,
            onCellEvent = self._onCellEvent,
            onRangeEvent = onRangeEvent)
        return evRange

    @property
    def cells(self) -> list[Cell]:
        cs = self.rootWorksheet.cells
        rt = list(map(lambda c: self._makeEventCell(c), cs))
        return rt

    def _makeEventCell(self, cell: Cell) -> Cell:
        return EventCell(cell, onCellEvent = self._onCellEvent)

    def renameRs(self, newName: str) -> Result[None, ErrorReport]:
        oldName = self.name
        rs = self.rootWorksheet.renameRs(newName)
        if rs.isOk():
            self.__onWorksheetEvent(
                RenameWorksheetResponse(
                    workbookKey = self.workbook.workbookKey,
                    oldName = oldName,
                    newName = newName,
                ).toEventData()
            )
        else:
            self.__onWorksheetEvent(
                RenameWorksheetResponse(
                    workbookKey = self.workbook.workbookKey,
                    oldName = oldName,
                    newName = newName,
                    isError = True,
                    errorReport = rs.err
                ).toEventData()
            )
        return rs

    def deleteCellRs(self, address: CellAddress | Tuple[int, int] | str) -> Result[None, ErrorReport]:
        address = CellAddresses.parseAddress(address)
        delRs = self.rootWorksheet.deleteCellRs(address)
        delResponse = DeleteCellResponse(
            workbookKey = self.workbook.workbookKey,
            worksheetName = self.name,
            cellAddress = address,
        )
        if delRs.isOk():
            delResponse.newWorkbook = self.workbook
        else:
            delResponse.isError = True
            delResponse.errorReport = delRs.err

        self.__onWorksheetEvent(delResponse.toEventData())
        return delRs

    # TODO test this
    def deleteRangeRs(self, rangeAddress: RangeAddress) -> Result[None, ErrorReport]:
        delRs = self.rootWorksheet.deleteRangeRs(rangeAddress)
        eventResponse = DeleteMultiResponse(
            isError = not delRs.isOk(),
            workbookKey = self.workbook.workbookKey
        )
        if delRs.isOk():
            eventResponse.newWorkbook = self.workbook
        else:
            eventResponse.errorReport = delRs.err

        self.__onWorksheetEvent(eventResponse.toEventData())
        return delRs

    def pasteProtoRs(
            self,
            anchorCell: CellAddress,
            paster: Paster | None = None) -> Result[None, ErrorReport]:
        rs = self.rootWorksheet.pasteProtoRs(anchorCell, paster)
        self.__emitPasteEvent(rs)
        return rs

    def pasteRs(self, anchorCell: CellAddress, paster: Paster | None = None) -> Result[None, ErrorReport]:
        rs = self.rootWorksheet.pasteRs(anchorCell, paster)
        self.__emitPasteEvent(rs)
        return rs

    def pasteDataFrameRs(self, anchorCell: CellAddress, paster: Paster | None = None) -> Result[None, ErrorReport]:
        rs = self.rootWorksheet.pasteDataFrameRs(anchorCell, paster)
        self.__emitPasteEvent(rs)
        return rs
    
    def __emitPasteEvent(self,rs:Result[None, ErrorReport]):
        response = PasteRangeResponse(
            isError = rs.isErr(),
            windowId = None
        )
        if rs.isOk():
            response.workbookKey = self.workbook.workbookKey
            response.newWorkbook = self.workbook.rootWorkbook
        else:
            response.errorReport = rs.err

        self.__onWorksheetEvent(response.toEventData())



