import uuid
from functools import partial
from typing import Callable, Any

from bicp_document_structure.message.P6Message import P6Message
from bicp_document_structure.message.P6MessageHeader import P6MessageHeader
from bicp_document_structure.message.SocketProvider import SocketProvider
from bicp_document_structure.message.event.P6Event import P6Event
from bicp_document_structure.message.event.P6Events import P6Events
from bicp_document_structure.message.event.reactor.CellReactor import CellReactor
from bicp_document_structure.message.event.reactor.ColumnReactor import ColumnReactor
from bicp_document_structure.message.event.reactor.EventReactorFactory import EventReactorFactory
from bicp_document_structure.message.event.reactor.RangeReactor import RangeReactor
from bicp_document_structure.message.event.reactor.ReactorProvider import ReactorProvider
from bicp_document_structure.message.event.reactor.WorkbookReactor import WorkbookReactor
from bicp_document_structure.message.event.reactor.WorksheetReactor import WorksheetReactor
from bicp_document_structure.message.event.reactor.eventData.WithWorkbookData import WithWorkbookData
from bicp_document_structure.message.event.reactor.eventData.WorkbookEventData import WorkbookEventData
from bicp_document_structure.message.event.reactor.eventData.WorksheetEventData import WorksheetEventData
from bicp_document_structure.message.sender.MessageSender import MessageSender


class StdReactorProvider(ReactorProvider):

    def __init__(self, socketProviderGetter: Callable[[], SocketProvider]):
        self.__socketProvider = socketProviderGetter
        self.__cellUpdateValue: CellReactor | None = None
        self.__cellUpdateScript: CellReactor | None = None
        self.__cellFormulaUpdate: CellReactor | None = None
        self.__cellClearScriptResult: CellReactor | None = None

        self.__colReRun: ColumnReactor | None = None
        self.__rangeReRun: RangeReactor | None = None

        self.__worksheetReRun: WorksheetReactor | None = None
        self.__worksheetRenameOk: WorksheetReactor | None = None
        self.__worksheetRenameFail: WorksheetReactor | None = None

        self.__workbookReRun: WorkbookReactor | None = None

    def stdCallback(self, event: P6Event, data: WithWorkbookData):
        """
        rerun the whole workbook, serialize the workbook to json, then send the json in a zmq message to a predesignated socket.
        If sockets are not available, don't do anything
        """
        socketProvider = self.__socketProvider()
        wb = data.workbook
        wb.reRun()
        if socketProvider is not None:
            socket = socketProvider.reqSocketForUIUpdating()
            if socket is not None:
                replyRs = MessageSender.sendREQ_Proto(
                    socket = socket,
                    msg = P6Message(
                        header = P6MessageHeader(str(uuid.uuid4()), event),
                        content = wb))
                if replyRs.isErr():
                    raise replyRs.err.toException()

    def createNewWorksheet(self) -> WorkbookReactor:
        def cb(wbEventData: WorkbookEventData):
            msg = StdReactorProvider.__createP6Msg(wbEventData.event, wbEventData.data)
            self._send(msg)
        reactor = EventReactorFactory.makeWorkbookReactor(cb)
        return reactor

    def cellUpdateValue(self) -> CellReactor:
        if self.__cellUpdateValue is None:
            event = P6Events.Cell.UpdateValueEvent
            self.__cellUpdateValue = EventReactorFactory.makeCellReactor(partial(self.stdCallback, event))
        return self.__cellUpdateValue

    def cellUpdateScript(self) -> CellReactor:
        if self.__cellUpdateScript is None:
            event = P6Events.Cell.UpdateScript
            self.__cellUpdateScript = EventReactorFactory.makeCellReactor(partial(self.stdCallback, event))
        return self.__cellUpdateScript

    def cellUpdateFormula(self) -> CellReactor:
        if self.__cellFormulaUpdate is None:
            event = P6Events.Cell.UpdateFormula
            self.__cellFormulaUpdate = EventReactorFactory.makeCellReactor(partial(self.stdCallback, event))
        return self.__cellFormulaUpdate

    def cellClearScriptResult(self) -> CellReactor:
        if self.__cellClearScriptResult is None:
            event = P6Events.Cell.ClearScriptResult
            self.__cellClearScriptResult = EventReactorFactory.makeCellReactor(
                partial(self.stdCallback, event))
        return self.__cellClearScriptResult

    def rangeReRun(self) -> RangeReactor:
        if self.__rangeReRun is None:
            event = P6Events.Range.ReRun
            self.__rangeReRun = EventReactorFactory.makeRangeReactor(partial(self.stdCallback, event))
        return self.__rangeReRun

    def worksheetReRun(self) -> WorksheetReactor:
        if self.__worksheetReRun is None:
            event = P6Events.Worksheet.ReRun
            self.__worksheetReRun = EventReactorFactory.makeRangeReactor(
                partial(self.stdCallback, event))
        return self.__worksheetReRun

    def worksheetRenameOk(self) -> WorksheetReactor:
        if self.__worksheetRenameOk is None:
            def cb(data: WorksheetEventData):
                eventData: P6Events.Worksheet.RenameOk.Data = data.data
                msg = P6Message(
                    header = P6MessageHeader(str(uuid.uuid4()), data.event),
                    content = eventData)
                self._send(msg)
            self.__worksheetRenameOk = EventReactorFactory.makeWorksheetReactor(cb)
        return self.__worksheetRenameOk

    def _send(self, p6Msg: P6Message):
        socketProvider = self.__socketProvider()
        if socketProvider is not None:
            socket = socketProvider.reqSocketForUIUpdating()
            if socket is not None:
                replyRs = MessageSender.sendREQ_Proto(
                    socket = socket,
                    msg = p6Msg)
                if replyRs.isErr():
                    raise replyRs.err.toException()

    @staticmethod
    def __createP6Msg(event, data:Any):
        msg = P6Message(
            header = P6MessageHeader(
                msgId = str(uuid.uuid4()),
                eventType = event,
            ),
            content = data)
        return msg
