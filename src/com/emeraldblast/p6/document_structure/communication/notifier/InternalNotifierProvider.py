from typing import Callable

from com.emeraldblast.p6.document_structure.communication.SocketProvider import SocketProvider
from com.emeraldblast.p6.document_structure.communication.event_server.P6Messages import P6Messages
from com.emeraldblast.p6.document_structure.communication.event_server.msg.P6Message import P6Message
from com.emeraldblast.p6.document_structure.communication.event_server.response.P6Response import P6Response
from com.emeraldblast.p6.document_structure.communication.notifier.eventData.EventData import EventData
from com.emeraldblast.p6.document_structure.communication.reactor.EventReactor import EventReactor
from com.emeraldblast.p6.document_structure.communication.reactor.EventReactors import EventReactors
from com.emeraldblast.p6.document_structure.communication.sender.MessageSender import MessageSender


class InternalNotifierProvider:
    """All these reactors do is wrapping the data in P6Response/P6Message and sending the data away. Nothing more."""

    def __init__(self, socketProviderGetter: Callable[[], SocketProvider]):
        self.__socketProvider = socketProviderGetter
        self.__worksheetRenameReactor: EventReactor | None = None

    def __commonNotifier(self) -> EventReactor[EventData, None]:
        def cb(data: EventData):
            msg = P6Messages.p6Response(
                event = data.event,
                data = data.data)
            self.__send(msg)

        # reactor = EventReactors.makeBasicReactor(cb)
        reactor = EventReactors.makeSyncBasicReactor(cb)
        return reactor

    def scriptNotifier(self) -> EventReactor[EventData, None]:
        return self.__commonNotifier()

    def workbookNotifier(self) -> EventReactor[EventData, None]:
        return self.__commonNotifier()

    def cellNotifier(self) -> EventReactor[EventData, None]:
        return self.__commonNotifier()

    def worksheetNotifier(self) -> EventReactor[EventData, None]:
        return self.__commonNotifier()

    def appNotifier(self) -> EventReactor[EventData, None]:
        return self.__commonNotifier()

    def __send(self, p6MsgOrRes: P6Message | P6Response):
        MessageSender.sendP6MsgRes(self.__socketProvider(), p6MsgOrRes)
