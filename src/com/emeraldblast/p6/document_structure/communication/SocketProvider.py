from abc import ABC

from zmq import Socket


class SocketProvider(ABC):
    def reqSocketForUIUpdating(self) -> Socket | None:
        raise NotImplementedError()

    def updateREQSocketForUIUpdating(self, newSocket: Socket | None):
        raise NotImplementedError()

    # def eventServerPort(self)->int:
    #     raise NotImplementedError()
    #
    # def updateEventServerPort(self,port):
    #     raise NotImplementedError()