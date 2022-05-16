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

    def startApp(self, d = {}):
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
        from com.emeraldblast.p6.document_structure.util.for_test.TestUtils import findNewSocketPort, \
            startREPServerOnThread, \
            sendClose
        from com.emeraldblast.p6.document_structure.workbook.key.WorkbookKeys import WorkbookKeys
        from com.emeraldblast.p6.proto.P6MsgProtos_pb2 import P6MessageProto, P6ResponseProto, P6MessageHeaderProto
        from com.emeraldblast.p6.proto.WorkbookProtos_pb2 import CreateNewWorksheetResponseProto, \
            SaveWorkbookRequestProto
        from com.emeraldblast.p6.proto.WorksheetProtos_pb2 import RenameWorksheetResponseProto
        local = locals()
        globals()

        setIPythonGlobals({**local, **globals(), **d})
        startApp()
        self._app = getApp()
        port = findNewSocketPort()
        getApp().eventServer.start(port)
        zsocket = getApp().zContext.socket(zmq.REQ)
        zsocket.connect(f"tcp://localhost:{port}")
        self._requestZSocket = zsocket

        self.app.wbContainer.addWorkbook(TestEnvImp.sampleWb("Book1"))
        self.app.wbContainer.addWorkbook(TestEnvImp.sampleWb("Book2"))
        self.app.wbContainer.addWorkbook(TestEnvImp.sampleWb("Book3"))
        self.app.wbContainer.addWorkbook(TestEnvImp.sampleWb("Book4"))


    def stopAll(self):
        stopApp()
        self.requestZSocket.close()
        self.closeRepListener()

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

    def startREPListener(self, isOk, onReceive):
        """
        emu the front end rep listener
        """
        port = findNewSocketPort()
        self._repPort = port


        repSocket = self.app.zContext.socket(zmq.REP)
        repSocket.bind(f"tcp://*:{port}")
        if self._toRepSocket is None:
            self._toRepSocket = self.app.zContext.socket(zmq.REQ)
            self._toRepSocket.connect(f"tcp://localhost:{self._repPort}")

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

    def startREPListenerOnThread(self,isOk, onReceive) -> threading.Thread:
        thread = threading.Thread(target = self.startREPListener, args = [isOk, onReceive])
        thread.daemon = True
        thread.start()
        while True:
            if self._toRepSocket is not None:
                self.app.socketProvider.updateREQSocketForUIUpdating(self._toRepSocket)
                break
        self._repListenerThread = thread
        return thread

    def closeRepListener(self):
        if self._toRepSocket is not None:
            self._toRepSocket.send(b"close")
            self._toRepSocket.close()
            self._toRepSocket = None
        if self._repListenerThread is not None:
            self._repListenerThread.join()
            self._repListenerThread = None


