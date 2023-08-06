from abc import ABC

from zmq import Socket


class SocketProvider(ABC):
    def notificationSocket(self) -> Socket | None:
        raise NotImplementedError()

    def updateNotificationSocket(self, newSocket: Socket | None):
        raise NotImplementedError()