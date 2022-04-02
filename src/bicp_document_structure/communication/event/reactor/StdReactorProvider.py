import uuid
from functools import partial
from typing import Callable

from bicp_document_structure.communication.SocketProvider import SocketProvider
from bicp_document_structure.communication.event.P6Event import P6Event
from bicp_document_structure.communication.event.P6Events import P6Events
from bicp_document_structure.communication.event.reactor.CellReactor import CellReactor
from bicp_document_structure.communication.event.reactor.ColumnReactor import ColumnReactor
from bicp_document_structure.communication.event.reactor.EventReactorFactory import EventReactorFactory
from bicp_document_structure.communication.event.reactor.RangeReactor import RangeReactor
from bicp_document_structure.communication.event.reactor.ReactorProvider import ReactorProvider
from bicp_document_structure.communication.event.reactor.WorkbookReactor import WorkbookReactor
from bicp_document_structure.communication.event.reactor.WorksheetReactor import WorksheetReactor
from bicp_document_structure.communication.event.reactor.eventData.CellEventData import CellEventData
from bicp_document_structure.communication.event.reactor.eventData.WithWorkbookData import WithWorkbookData
from bicp_document_structure.communication.event.reactor.eventData.WorkbookEventData import WorkbookEventData
from bicp_document_structure.communication.event_server.P6Messages import P6Messages
from bicp_document_structure.communication.event_server.msg.P6Message import P6Message
from bicp_document_structure.communication.event_server.msg.P6MessageHeader import P6MessageHeader
from bicp_document_structure.communication.event_server.response.P6Response import P6Response
from bicp_document_structure.communication.sender.MessageSender import MessageSender


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
        self.__worksheetRenameReactor: WorksheetReactor | None = None
        self.__worksheetRenameFail: WorksheetReactor | None = None

        self.__workbookReRun: WorkbookReactor | None = None

    def workbookReRun(self) -> WorkbookReactor:
        pass

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
                        data = wb))
                if replyRs.isErr():
                    raise replyRs.err.toException()

    def createNewWorksheet(self) -> WorkbookReactor:
        def cb(data: WorkbookEventData):
            status = P6Response.Status.OK
            if data.isError:
                status = P6Response.Status.ERROR
            msg = P6Messages.p6Response(data.event, data.data, status)
            self._sendResponse(msg)

        reactor = EventReactorFactory.makeWorkbookReactor(cb)
        return reactor

    def cellUpdateReactor(self) -> CellReactor:
        def cb(cellEventData: CellEventData):
            status = P6Response.Status.OK
            if cellEventData.isError:
                status = P6Response.Status.ERROR

            p6Res = P6Messages.p6Response(
                event = cellEventData.event,
                data = cellEventData.data,
                status = status)

            self._sendResponse(p6Res)

        reactor = EventReactorFactory.makeCellReactor(cb)
        return reactor

    def rangeReRun(self) -> RangeReactor:
        if self.__rangeReRun is None:
            event = P6Events.Range.ReRun
            self.__rangeReRun = EventReactorFactory.makeRangeReactor(partial(self.stdCallback, event))
        return self.__rangeReRun
        # raise NotImplementedError()

    def worksheetReRun(self) -> WorksheetReactor:
        # raise NotImplementedError()
        if self.__worksheetReRun is None:
            event = P6Events.Worksheet.ReRun
            self.__worksheetReRun = EventReactorFactory.makeRangeReactor(
                partial(self.stdCallback, event))
        return self.__worksheetReRun

    def worksheetRename(self) -> WorkbookReactor:
        if self.__worksheetRenameReactor is None:
            def cb(eventData: WorkbookEventData):
                if not eventData.isError:
                    msg = P6Messages.p6Response(eventData.event, eventData.data)
                else:
                    msg = P6Messages.p6Response(eventData.event, eventData.data, P6Response.Status.ERROR)
                self._sendResponse(msg)

            self.__worksheetRenameReactor = EventReactorFactory.makeWorkbookReactor(cb)
        return self.__worksheetRenameReactor

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

    def _sendResponse(self, p6Res: P6Response):
        socketProvider = self.__socketProvider()
        if socketProvider is not None:
            socket = socketProvider.reqSocketForUIUpdating()
            if socket is not None:
                replyRs = MessageSender.sendREQ_Proto(
                    socket = socket,
                    msg = p6Res)
                if replyRs.isErr():
                    raise replyRs.err.toException()
            else:  # socket is None
                pass  # do nothing
        else:  # socket provider is None
            pass  # do nothing
