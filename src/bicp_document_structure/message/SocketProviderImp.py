from zmq import Socket

from bicp_document_structure.message.SocketProvider import SocketProvider


class SocketProviderImp(SocketProvider):
    def __init__(self, reqSocketUI: Socket | None = None):
        self.__reqSocketUI: Socket = reqSocketUI

    def reqSocketForUIUpdating(self) -> Socket | None:
        return self.__reqSocketUI

    def updateREQSocketForUIUpdating(self, newSocket: Socket | None):
        self.__reqSocketUI = newSocket
