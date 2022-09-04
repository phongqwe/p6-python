import zmq

from com.qxdzbc.p6.document_structure.app.TopLevel import *
from com.qxdzbc.p6.document_structure.communication.event_server.msg.P6Message import P6Message
from com.qxdzbc.p6.document_structure.communication.event_server.response.P6Response import P6Response
from com.qxdzbc.p6.document_structure.util.for_test.emu.NotificationListener import NotificationListener
from com.qxdzbc.p6.document_structure.workbook.WorkbookImp import WorkbookImp


class TestEnvImp:
    """
    How to use:
        testEnv = TestEnvImp()
        testEnv.startApp()

        use sendRequestToEventServer() to send request to event server
        use self.notifListener.addReactor() to add notification reactor

        This test env emulate a real app which consist of:
            2 workbooks, each workbook consist of 2 sheets. All wb and ws can emit events
            1 event server
            1 notification listener
    """

    def __init__(self):
        self._eventServerRequestSocket = None
        self.eventServerPort = None
        self._app = None
        self._eventServerPort = None
        self.notifSocket = None
        self.notifListener:NotificationListener = None

    @staticmethod
    def sampleWb(name):
        wb = WorkbookImp(name)
        s1 = wb.createNewWorksheet("Sheet1")
        s2 = wb.createNewWorksheet("Sheet2")
        s1.cell((1, 1)).value = 11
        s1.cell((2, 2)).value = 22
        s1.cell((3, 3)).value = 33
        s2.cell((1, 1)).value = 211
        s2.cell((2, 2)).value = 222
        s2.cell((3, 3)).value = 233
        return wb

    def startEnv(self):
        # these import will be put in local
        from com.qxdzbc.p6.document_structure.app.GlobalScope import setIPythonGlobals
        from com.qxdzbc.p6.document_structure.app.TopLevel import startApp, getApp
        from com.qxdzbc.p6.document_structure.util.for_test.TestUtils import findNewSocketPort
        from com.qxdzbc.p6.document_structure.app.worksheet_functions.WorksheetFunctions import WorksheetFunctions
        from com.qxdzbc.p6.document_structure.workbook.key.WorkbookKeys import WorkbookKeys
        from com.qxdzbc.p6.document_structure.range.address.RangeAddresses import RangeAddresses
        import zmq

        local = locals()
        globals()

        setIPythonGlobals({**local, **globals()})
        startApp()
        self._app = getApp()

        b1 = getApp().createNewWorkbook("Book1")
        b1.createNewWorksheet("Sheet1")
        b1.createNewWorksheet("Sheet2")

        b2 = getApp().createNewWorkbook("Book2")
        b2.createNewWorksheet("Sheet1")
        b2.createNewWorksheet("Sheet2")
        # start event server
        self.eventServerPort = findNewSocketPort()
        self.app.eventServer.start(self.eventServerPort)

        self._eventServerRequestSocket = self.app.zContext.socket(zmq.REQ)
        self._eventServerRequestSocket.connect(f"tcp://localhost:{self.eventServerPort}")

        # start event notifier sender
        self.notifListener = NotificationListener(self.app.zContext)
        self.notifListener.startOnThread()
        self.app.socketProvider.updateNotificationSocket(self.notifListener.senderSocket)


    def stopAll(self):
        stopApp()
        if self.notifSocket:
            self.notifSocket.close()
            self.notifSocket = None
        self.notifListener.stop()

        if self.eventServerRequestSocket:
            self.eventServerRequestSocket.close()
            self._eventServerRequestSocket = None

    @property
    def app(self)->App:
        return self._app

    @property
    def notifSenderSocket(self):
        """socket for sending msg to rep listener"""
        return self.notifListener.senderSocket


    @property
    def eventServerRequestSocket(self):
        return self._eventServerRequestSocket

    def sendRequestToEventServer(self,p6Msg:P6Message|bytes)->P6Response | None:

        b = p6Msg
        if isinstance(p6Msg,P6Message):
            b = p6Msg.toProtoBytes()
        if self.eventServerRequestSocket:
            self.eventServerRequestSocket.send(b)
            recv = self.eventServerRequestSocket.recv()
            rt = P6Response.fromProtoBytes(recv)
            return rt
        else:
            return None


