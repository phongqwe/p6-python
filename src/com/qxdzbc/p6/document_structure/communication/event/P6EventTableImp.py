import inspect
from typing import Any, Type

from com.qxdzbc.p6.document_structure.communication.event.P6Events import P6Events
from com.qxdzbc.p6.document_structure.communication.event.P6Event import P6Event
from com.qxdzbc.p6.document_structure.communication.event.P6EventTable import P6EventTable


class P6EventTableImp(P6EventTable):
    _i = None

    @staticmethod
    def i() -> 'P6EventTable':
        if P6EventTableImp._i is None:
            P6EventTableImp._i = P6EventTableImp()
        return P6EventTableImp._i

    def __init__(self):

        self.eMap = {}

        for eventGroupKey in P6Events.__dict__:
            eventGroup = P6Events.__dict__[eventGroupKey]
            if inspect.isclass(eventGroup):
                for eventName in eventGroup.__dict__:
                    eventClazz = eventGroup.__dict__[eventName]
                    if inspect.isclass(eventClazz):
                        event = eventClazz.event
                        if hasattr(eventClazz, "Response"):
                            responseClazz = eventClazz.Response
                            if responseClazz:
                                self.eMap[responseClazz] = event
                        if hasattr(eventClazz, "Request"):
                            requestClazz = eventClazz.Request
                            if requestClazz:
                                self.eMap[requestClazz] = event
                        if hasattr(eventClazz, "Reactor"):
                            reactorClazz = eventClazz.Reactor
                            if reactorClazz:
                                self.eMap[reactorClazz] = event
                        if hasattr(eventClazz,"Notification"):
                            notifClazz = eventClazz.Notification
                            if notifClazz:
                                self.eMap[notifClazz] = event
                        if hasattr(eventClazz,"Other"):
                            otherList = eventClazz.Other
                            if otherList:
                                if isinstance(otherList, list):
                                    for o in otherList:
                                        self.eMap[o] = event


    def getEventFor(self, something: Any) -> P6Event:
        return self.getEventForClazz(type(something))

    def getEventForClazz(self, clazz: Type) -> P6Event:
        event = self.eMap.get(clazz)
        if event is None:
            event = P6Events.Fallback.UnknownEvent.event
        return event
