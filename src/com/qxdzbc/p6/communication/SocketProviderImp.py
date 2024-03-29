from zmq import Socket

from com.qxdzbc.p6.communication.SocketProvider import SocketProvider


class SocketProviderImp(SocketProvider):

    def __init__(self, reqSocketUI: Socket | None = None, eventServerPort:int | None = None):
        self.__reqSocketUI: Socket = reqSocketUI
        self._eventServerPort: int = eventServerPort

    def notificationSocket(self) -> Socket | None:
        return self.__reqSocketUI

    def updateNotificationSocket(self, newSocket: Socket | None):
        self.__reqSocketUI = newSocket

    # def eventServerPort(self) -> int:
    #     return self._eventServerPort
    #
    # def updateEventServerPort(self, port):
    #     self._eventServerPort = port