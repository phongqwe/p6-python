from functools import partial
from typing import Callable, Tuple, Optional

from com.emeraldblast.p6.document_structure.cell.Cell import Cell
from com.emeraldblast.p6.document_structure.cell.EventCell import EventCell
from com.emeraldblast.p6.document_structure.cell.address.CellAddress import CellAddress
from com.emeraldblast.p6.document_structure.cell.address.CellAddresses import CellAddresses
from com.emeraldblast.p6.document_structure.communication.event.P6Events import P6Events
from com.emeraldblast.p6.document_structure.communication.event.data_structure.workbook_event.WorkbookUpdateCommonResponse import \
    WorkbookUpdateCommonResponse
from com.emeraldblast.p6.document_structure.communication.event.data_structure.worksheet_event.DeleteCell import \
    DeleteCellResponse
from com.emeraldblast.p6.document_structure.communication.event.data_structure.worksheet_event.RenameWorksheetResponse import \
    RenameWorksheetResponse
from com.emeraldblast.p6.document_structure.communication.notifier.eventData.AppEventData import EventData
from com.emeraldblast.p6.document_structure.range.EventRange import EventRange
from com.emeraldblast.p6.document_structure.range.Range import Range
from com.emeraldblast.p6.document_structure.range.address.RangeAddress import RangeAddress
from com.emeraldblast.p6.document_structure.range.address.RangeAddresses import RangeAddresses
from com.emeraldblast.p6.document_structure.util.AddressParser import AddressParser
from com.emeraldblast.p6.document_structure.util.report.error.ErrorReport import ErrorReport
from com.emeraldblast.p6.document_structure.util.result.Result import Result
from com.emeraldblast.p6.document_structure.worksheet.Worksheet import Worksheet
from com.emeraldblast.p6.document_structure.worksheet.WorksheetWrapper import WorksheetWrapper


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

    def reRun(self):
        self.rootWorksheet.reRun()
        if self.__onWorksheetEvent is not None:
            # todo incomplete data
            eventData = EventData(
                event = P6Events.Worksheet.ReRun.event,
            )
            self.__onWorksheetEvent(eventData)

    def _XonCellEvent(self, data: EventData):
        data.worksheet = self.rootWorksheet
        if self.__onCellEvent is not None:
            self.__onCellEvent(data)

    def range(self, rangeAddress: str | RangeAddress | Tuple[CellAddress, CellAddress]) -> Range:
        rng = self.rootWorksheet.range(rangeAddress)

        def onRangeEvent(data: EventData):
            data.worksheet = self.rootWorksheet
            if self.__onRangeEvent is not None:
                self.__onRangeEvent(data)

        evRange = EventRange(
            innerRange = rng,
            onCellEvent = self._XonCellEvent,
            onRangeEvent = onRangeEvent)
        return evRange

    @property
    def cells(self) -> list[Cell]:
        cs = self.rootWorksheet.cells
        rt = list(map(lambda c: self._makeEventCell(c), cs))
        return rt

    def _makeEventCell(self, cell: Cell) -> Cell:
        return EventCell(cell, onCellEvent = self._XonCellEvent)

    def renameRs(self, newName: str) -> Result[None, ErrorReport]:
        oldName = self.name
        index = self.workbook.getIndexOfWorksheet(oldName)
        rs = self.rootWorksheet.renameRs(newName)
        if rs.isOk():
            self.__onWorksheetEvent(
                EventData(
                    event = P6Events.Worksheet.Rename.event,
                    data = RenameWorksheetResponse(
                        workbookKey = self.workbook.workbookKey,
                        oldName = oldName,
                        newName = newName,
                        # index= index,
                    )
                )
            )
        else:
            self.__onWorksheetEvent(
                EventData(
                    event = P6Events.Worksheet.Rename.event,
                    data = RenameWorksheetResponse(
                        workbookKey = self.workbook.workbookKey,
                        oldName = oldName,
                        newName = newName,
                        isError = True,
                        errorReport = rs.err
                    )
                )
            )
        return rs

    def deleteCellRs(self, address: CellAddress | Tuple[int, int]|str) -> Result[None, ErrorReport]:
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

        eventData = EventData(
            event = P6Events.Worksheet.DeleteCell.event,
            data = delResponse
        )

        self.__onWorksheetEvent(eventData)
        return delRs

    # TODO test this
    def deleteRangeRs(self, rangeAddress: RangeAddress) -> Result[None, ErrorReport]:
        delRs = self.rootWorksheet.deleteRangeRs(rangeAddress)
        eventResponse = WorkbookUpdateCommonResponse(
            isError = not delRs.isOk(),
            workbookKey = self.workbook.workbookKey
        )
        if delRs.isOk():
            eventResponse.newWorkbook = self.workbook
        else:
            eventResponse.errorReport = delRs.err

        self.__onWorksheetEvent(EventData(
            event = P6Events.Worksheet.DeleteMulti.event,
            data = eventResponse
        ))
        return delRs

    
    # def pasteFromClipboardRs(self, anchorCell: CellAddress)->Result[None,ErrorReport]:
    #     rs= self.rootWorksheet.pasteFromClipboardRs(anchorCell)
    #     data = WorkbookUpdateCommonResponse(
    #         isError = rs.isErr(),
    #         workbookKey = self.workbook.workbookKey
    #     )
    #     if rs.isOk():
    #         data.newWorkbook = self.workbook.rootWorkbook
    #     else:
    #         data.errorReport = rs.err
    #
    #     self.__onWorksheetEvent(EventData(
    #         event=P6Events.Worksheet.PasteRange.event,
    #         data = data
    #     ))
    #     return rs

