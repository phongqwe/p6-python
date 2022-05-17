from typing import Callable

from com.emeraldblast.p6.document_structure.communication.SocketProvider import SocketProvider
from com.emeraldblast.p6.document_structure.communication.event_server.P6Messages import P6Messages
from com.emeraldblast.p6.document_structure.communication.event_server.msg.P6Message import P6Message
from com.emeraldblast.p6.document_structure.communication.event_server.response.P6Response import P6Response
from com.emeraldblast.p6.document_structure.communication.internal_reactor.eventData.AppEventData import EventData
from com.emeraldblast.p6.document_structure.communication.reactor.EventReactor import EventReactor
from com.emeraldblast.p6.document_structure.communication.reactor.EventReactorFactory import EventReactorFactory
from com.emeraldblast.p6.document_structure.communication.sender.MessageSender import MessageSender


class InternalNotifierProvider:

    """All these reactors do is wrapping the data in P6Res/P6Msg and sending the data away. Nothing more."""

    def __init__(self, socketProviderGetter: Callable[[], SocketProvider]):
        self.__socketProvider = socketProviderGetter
        self.__worksheetRenameReactor: EventReactor | None = None

    def workbookNotifier(self) -> EventReactor[EventData, None]:
        def cb(data: EventData):
            msg = P6Messages.p6Response(data.event, data.data)
            self.__send(msg)

        reactor = EventReactorFactory.makeBasicReactor(cb)
        return reactor

    def cellNotifier(self) -> EventReactor[EventData, None]:
        def cb(cellEventData: EventData):
            p6Res = P6Messages.p6Response(
                event = cellEventData.event,
                data = cellEventData.data, )
            self.__send(p6Res)
        reactor = EventReactorFactory.makeBasicReactor(cb)
        return reactor

    def worksheetNotifier(self) -> EventReactor[EventData, None]:
        def cb(eventData: EventData):
            msg = P6Messages.p6Response(eventData.event, eventData.data)
            # MessageSender.sendP6MsgRes(self.__socketProvider(),msg)
            self.__send(msg)

        reactor = EventReactorFactory.makeBasicReactor(cb)
        return reactor

    def appNotifier(self)->EventReactor[EventData,None]:
        def cb(data:EventData):
            response = P6Messages.p6Response(event = data.event,data=data.data)
            self.__send(response)
        reactor = EventReactorFactory.makeBasicReactor(cb)
        return reactor

    def __send(self,p6MsgOrRes:P6Message|P6Response):
        MessageSender.sendP6MsgRes(self.__socketProvider(), p6MsgOrRes)

