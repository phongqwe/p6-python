import threading
import time

import zmq

from com.emeraldblast.p6.document_structure.workbook.WorkbookImp import WorkbookImp
from com.emeraldblast.p6.document_structure.app.UserFunctions import *
from com.emeraldblast.p6.document_structure.util.for_test.TestUtils import findNewSocketPort

class TestEnvImp:

    def __init__(self):
        self._app = None
        self._requestZSocket = None
        self._toRepSocket = None
        self._repPort = None
        self._repListenerThread = None
        self._eventServerPort = None
        self.notifSocket = None
        self.notifPort = None

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

    def startApp(self):
        # these import will be put in local
        from com.emeraldblast.p6.document_structure.app.App import App
        from com.emeraldblast.p6.document_structure.app.GlobalScope import setIPythonGlobals
        from com.emeraldblast.p6.document_structure.app.UserFunctions import startApp, restartApp, stopApp, getApp
        from com.emeraldblast.p6.document_structure.util.for_test.TestUtils import findNewSocketPort
        from com.emeraldblast.p6.document_structure.workbook.WorkbookImp import WorkbookImp
        from com.emeraldblast.p6.document_structure.app.worksheet_functions.WorksheetFunctions import WorksheetFunctions
        from com.emeraldblast.p6.document_structure.app.worksheet_functions.WorksheetFunctions import WorksheetFunctions
        from com.emeraldblast.p6.document_structure.cell.address.CellAddresses import CellAddresses
        from com.emeraldblast.p6.document_structure.communication.event.P6Events import P6Events
        from com.emeraldblast.p6.document_structure.communication.event.data_structure.cell_event.CellUpdateRequest import \
            CellUpdateRequest
        from com.emeraldblast.p6.document_structure.communication.event_server.response.P6Response import P6Response
        from com.emeraldblast.p6.document_structure.workbook.key.WorkbookKeys import WorkbookKeys
        from com.emeraldblast.p6.proto.P6MsgProtos_pb2 import P6MessageProto, P6ResponseProto, P6MessageHeaderProto
        from com.emeraldblast.p6.proto.WorkbookProtos_pb2 import CreateNewWorksheetResponseProto, \
            SaveWorkbookRequestProto
        from com.emeraldblast.p6.proto.WorksheetProtos_pb2 import RenameWorksheetResponseProto
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
        port = findNewSocketPort()
        self.app.eventServer.start(port)
        reqSocket = getApp().zContext.socket(zmq.REQ)
        reqSocket.connect(f"tcp://localhost:{port}")
        self._requestZSocket = reqSocket

        # start event notifier sender

    def createNotifSender(self):
        notifSenderPort = findNewSocketPort()
        notifSocket = self.app.zContext.socket(zmq.REQ)
        notifSocket.connect(f"tcp://localhost:{notifSenderPort}")
        self.app.socketProvider.updateREQSocketForUIUpdating(notifSocket)
        self.notifSocket = notifSocket
        self.notifPort = notifSenderPort

    def removeNotifSender(self):
        if self.notifSocket:
            self.notifSocket.close()
            self.notifSocket = None
            self.app.socketProvider.updateREQSocketForUIUpdating(None)


    def stopAll(self):
        stopApp()
        self.requestZSocket.close()
        self.closeNotifListener()
        if self.notifSocket:
            self.notifSocket.close()
            self.notifSocket = None

    @property
    def app(self)->App:
        return self._app

    @property
    def requestZSocket(self):
        return self._requestZSocket

    @property
    def toRepSocket(self):
        """socket for sending msg to rep listener"""
        return self._toRepSocket

    def startNotificationListener(self, isOk, onReceive):
        """
        emu the front end rep listener
        """
        repSocket = self.app.zContext.socket(zmq.REP)
        repSocket.bind(f"tcp://*:{self.notifPort}")
        if self._toRepSocket is None:
            self._toRepSocket = self.app.zContext.socket(zmq.REQ)
            self._toRepSocket.connect(f"tcp://localhost:{self.notifPort}")

        while True:
            receive = repSocket.recv()
            if receive == b"close":
                break
            onReceive(receive)
            if isOk:
                repSocket.send("ok".encode())
            else:
                repSocket.send("fail".encode())
        repSocket.close()

    def startNotificationListenerOnThread(self, isOk, onReceive) -> threading.Thread:
        thread = threading.Thread(target = self.startNotificationListener, args = [isOk, onReceive])
        thread.daemon = True
        thread.start()
        while True:
            if self._toRepSocket is not None:
                self.app.socketProvider.updateREQSocketForUIUpdating(self._toRepSocket)
                break
        self._repListenerThread = thread
        return thread

    def closeNotifListener(self):
        if self._toRepSocket is not None:
            self._toRepSocket.send(b"close")
            self._toRepSocket.close()
            self._toRepSocket = None
        if self._repListenerThread is not None:
            self._repListenerThread.join()
            self._repListenerThread = None


