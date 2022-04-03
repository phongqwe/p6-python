from typing import Callable

from com.emeraldblast.p6.document_structure.communication.SocketProvider import SocketProvider
from com.emeraldblast.p6.document_structure.communication.event_server.P6Messages import P6Messages
from com.emeraldblast.p6.document_structure.communication.internal_reactor.eventData.CellEventData import CellEventData
from com.emeraldblast.p6.document_structure.communication.internal_reactor.eventData.WorkbookEventData import \
    WorkbookEventData
from com.emeraldblast.p6.document_structure.communication.internal_reactor.eventData.WorksheetEventData import \
    WorksheetEventData
from com.emeraldblast.p6.document_structure.communication.reactor.EventReactor import EventReactor
from com.emeraldblast.p6.document_structure.communication.reactor.EventReactorFactory import EventReactorFactory
from com.emeraldblast.p6.document_structure.communication.sender.MessageSender import MessageSender


class InternalReactorProvider:

    """All these reactors only do is wrapping the data in P6Res/P6Msg and sending the data away. Nothing more."""

    def __init__(self, socketProviderGetter: Callable[[], SocketProvider]):
        self.__socketProvider = socketProviderGetter
        self.__worksheetRenameReactor: EventReactor | None = None

    def workbookReactor(self) -> EventReactor[WorkbookEventData, None]:
        def cb(data: WorkbookEventData):
            msg = P6Messages.p6Response(data.event, data.data)
            MessageSender.sendP6MsgRes(self.__socketProvider(), msg)

        reactor = EventReactorFactory.makeBasicReactor(cb)
        return reactor

    def cellReactor(self) -> EventReactor[CellEventData, None]:
        def cb(cellEventData: CellEventData):
            p6Res = P6Messages.p6Response(
                event = cellEventData.event,
                data = cellEventData.data, )
            MessageSender.sendP6MsgRes(self.__socketProvider(), p6Res)

        reactor = EventReactorFactory.makeBasicReactor(cb)
        return reactor

    def worksheetReactor(self) -> EventReactor[WorksheetEventData, None]:
        if self.__worksheetRenameReactor is None:
            def cb(eventData: WorksheetEventData):
                msg = P6Messages.p6Response(eventData.event, eventData.data)
                MessageSender.sendP6MsgRes(self.__socketProvider(),msg)

            self.__worksheetRenameReactor = EventReactorFactory.makeBasicReactor(cb)
        return self.__worksheetRenameReactor
