import uuid
from typing import Callable

from bicp_document_structure.event.reactor.CellReactor import CellReactor
from bicp_document_structure.event.reactor.ColumnReactor import ColumnReactor
from bicp_document_structure.event.reactor.EventReactorFactory import EventReactorFactory
from bicp_document_structure.event.reactor.RangeEventReactor import RangeEventReactor
from bicp_document_structure.event.reactor.ReactorProvider import ReactorProvider
from bicp_document_structure.event.reactor.WorkbookReactor import WorkbookReactor
from bicp_document_structure.event.reactor.WorksheetReactor import WorksheetReactor
from bicp_document_structure.event.reactor.eventData.CellEventData import CellEventData
from bicp_document_structure.message.MsgType import MsgType
from bicp_document_structure.message.P6Message import P6Message
from bicp_document_structure.message.P6MessageHeader import P6MessageHeader
from bicp_document_structure.message.SocketProvider import SocketProvider
from bicp_document_structure.message.sender.MessageSender import MessageSender


class StdReactorProvider(ReactorProvider):

    def __init__(self,socketProviderGetter:Callable[[],SocketProvider]):
        self.__spg = socketProviderGetter

    def cellUpdateValue(self):
        """
        rerun the whole workbook, serialize the workbook to json, then send the json in a zmq message to a predesignated socket.
        If sockets are not available, don't do anything
        """
        def cb(data:CellEventData):
            socketProvider = self.__spg()
            wb = data.workbook
            wb.reRun()
            if socketProvider is not None:
                socket = socketProvider.reqSocketForUIUpdating()
                if socket is not None:
                    replyRs = MessageSender.sendREQ(
                        socket = socket,
                        msg = P6Message(
                            header = P6MessageHeader(str(uuid.uuid4()), MsgType.CellValueUpdate),
                            content = wb))
                    if replyRs.isErr():
                        raise replyRs.err.toException()
        return EventReactorFactory.makeCellReactor(cb)

    def cellUpdateScript(self) -> CellReactor:
        return None

    def cellUpdateFormula(self) -> CellReactor:
        return None

    def cellClearScriptResult(self) -> CellReactor:
        return None

    def colReRun(self) -> ColumnReactor:
        return None

    def rangeReRun(self) -> RangeEventReactor:
        return None

    def worksheetReRun(self) -> WorksheetReactor:
        return None

    def workbookReRun(self) -> WorkbookReactor:
        return None