from bicp_document_structure.communication.sender.SenderProvider import SenderProvider

from bicp_document_structure.communication.SocketProvider import SocketProvider
from bicp_document_structure.communication.sender.MessageSender import MessageSender


class SenderProviderImp(SenderProvider):

    def __init__(self, socketProvider):
        self.__socketProvider: SocketProvider | None = socketProvider
        self.__reqSenderForUpdatingUI = None

    def reqSenderForUpdatingUI(self) -> MessageSender:
        if self.__reqSenderForUpdatingUI is None:
            if self.__socketProvider is not None:
                socket = self.__socketProvider.reqSocketForUIUpdating()
                self.__reqSenderForUpdatingUI = MessageSender.reqSender(socket)
        return self.__reqSenderForUpdatingUI
