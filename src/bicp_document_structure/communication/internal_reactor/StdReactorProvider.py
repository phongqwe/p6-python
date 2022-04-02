from typing import Callable

from bicp_document_structure.communication.SocketProvider import SocketProvider
from bicp_document_structure.communication.event_server.P6Messages import P6Messages
from bicp_document_structure.communication.event_server.msg.P6Message import P6Message
from bicp_document_structure.communication.event_server.response.P6Response import P6Response
from bicp_document_structure.communication.internal_reactor.CellReactor import CellReactor
from bicp_document_structure.communication.internal_reactor.ColumnReactor import ColumnReactor
from bicp_document_structure.communication.internal_reactor.EventReactorFactory import EventReactorFactory
from bicp_document_structure.communication.internal_reactor.RangeReactor import RangeReactor
from bicp_document_structure.communication.internal_reactor.WorkbookReactor import WorkbookReactor
from bicp_document_structure.communication.internal_reactor.WorksheetReactor import WorksheetReactor
from bicp_document_structure.communication.internal_reactor.eventData.CellEventData import CellEventData
from bicp_document_structure.communication.internal_reactor.eventData.WorkbookEventData import WorkbookEventData
from bicp_document_structure.communication.sender.MessageSender import MessageSender


class StdReactorProvider:

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

    def createNewWorksheetReactor(self) -> WorkbookReactor:
        def cb(data: WorkbookEventData):
            status = P6Response.Status.OK
            if data.isError:
                status = P6Response.Status.ERROR
            msg = P6Messages.p6Response(data.event, data.data, status)
            self._send(msg)
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

            self._send(p6Res)

        reactor = EventReactorFactory.makeCellReactor(cb)
        return reactor


    def renameWorksheetReactor(self) -> WorkbookReactor:
        if self.__worksheetRenameReactor is None:
            def cb(eventData: WorkbookEventData):
                if not eventData.isError:
                    msg = P6Messages.p6Response(eventData.event, eventData.data)
                else:
                    msg = P6Messages.p6Response(eventData.event, eventData.data, P6Response.Status.ERROR)
                self._send(msg)

            self.__worksheetRenameReactor = EventReactorFactory.makeWorkbookReactor(cb)
        return self.__worksheetRenameReactor

    def _send(self, p6Msg: P6Message | P6Response):
        """ send a p6msg/p6response """
        socketProvider = self.__socketProvider()
        if socketProvider is not None:
            socket = socketProvider.reqSocketForUIUpdating()
            if socket is not None:
                replyRs = MessageSender.sendREQ_Proto(
                    socket = socket,
                    msg = p6Msg)
                if replyRs.isErr():
                    raise replyRs.err.toException()
