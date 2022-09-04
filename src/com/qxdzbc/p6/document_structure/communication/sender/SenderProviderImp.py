from com.qxdzbc.p6.document_structure.communication.SocketProvider import SocketProvider
from com.qxdzbc.p6.document_structure.communication.sender import SenderProvider
from com.qxdzbc.p6.document_structure.communication.sender.MessageSender import MessageSender


class SenderProviderImp(SenderProvider):

    def __init__(self, socketProvider):
        self.__socketProvider: SocketProvider | None = socketProvider
        self.__reqSenderForUpdatingUI = None

    def reqSenderForUpdatingUI(self) -> MessageSender:
        if self.__reqSenderForUpdatingUI is None:
            if self.__socketProvider is not None:
                socket = self.__socketProvider.notificationSocket()
                self.__reqSenderForUpdatingUI = MessageSender.reqSender(socket)
        return self.__reqSenderForUpdatingUI
