from typing import Callable

from com.emeraldblast.p6.document_structure.communication.SocketProvider import SocketProvider
from com.emeraldblast.p6.document_structure.communication.event_server.P6Messages import P6Messages
from com.emeraldblast.p6.document_structure.communication.event_server.msg.P6Message import P6Message
from com.emeraldblast.p6.document_structure.communication.event_server.response.P6Response import P6Response
from com.emeraldblast.p6.document_structure.communication.internal_reactor.EventReactor import EventReactor
from com.emeraldblast.p6.document_structure.communication.internal_reactor.EventReactorFactory import EventReactorFactory
from com.emeraldblast.p6.document_structure.communication.internal_reactor.eventData.CellEventData import CellEventData
from com.emeraldblast.p6.document_structure.communication.internal_reactor.eventData.WorkbookEventData import WorkbookEventData
from com.emeraldblast.p6.document_structure.communication.sender.MessageSender import MessageSender


class StdReactorProvider:

    def __init__(self, socketProviderGetter: Callable[[], SocketProvider]):
        self.__socketProvider = socketProviderGetter
        self.__worksheetRenameReactor: EventReactor | None = None


    def createNewWorksheetReactor(self) -> EventReactor[WorkbookEventData,None]:
        def cb(data: WorkbookEventData):
            msg = P6Messages.p6Response(data.event, data.data, P6Response.Status.OK)
            self._send(msg)
        reactor = EventReactorFactory.makeBasicReactor(cb)
        return reactor

    def cellUpdateReactor(self) -> EventReactor[CellEventData,None]:
        def cb(cellEventData: CellEventData):
            p6Res = P6Messages.p6Response(
                event = cellEventData.event,
                data = cellEventData.data,)
            self._send(p6Res)
        reactor = EventReactorFactory.makeBasicReactor(cb)
        return reactor


    # def renameWorksheetReactor(self) -> WorkbookReactor:
    def renameWorksheetReactor(self) -> EventReactor[WorkbookEventData,None]:
        if self.__worksheetRenameReactor is None:
            def cb(eventData: WorkbookEventData):
                msg = P6Messages.p6Response(eventData.event, eventData.data)
                self._send(msg)

            self.__worksheetRenameReactor = EventReactorFactory.makeBasicReactor(cb)
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
