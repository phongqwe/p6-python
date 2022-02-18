from zmq import Socket

from bicp_document_structure.message.SocketProvider import SocketProvider


class SocketProviderImp(SocketProvider):
    def __init__(self, reqSocketUI: Socket):
        self.__reqSocketUI: Socket = reqSocketUI

    def reqSocketForUIUpdating(self) -> Socket :
        return self.__reqSocketUI
