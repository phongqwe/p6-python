from abc import ABC

from zmq import Socket


class SocketProvider(ABC):
    def reqSocketForUIUpdating(self)->Socket:
        raise NotImplementedError()