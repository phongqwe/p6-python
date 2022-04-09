import unittest

import zmq

from com.emeraldblast.p6.document_structure.app.GlobalScope import setIPythonGlobals
# these 2 imports must be keep for the formula script to be able to run
from com.emeraldblast.p6.document_structure.app.UserFunctions import *
from com.emeraldblast.p6.document_structure.app.worksheet_functions.WorksheetFunctions import WorksheetFunctions
from com.emeraldblast.p6.document_structure.util.for_test.TestUtils import findNewSocketPort, startREPServerOnThread, \
    sendClose
from com.emeraldblast.p6.document_structure.workbook.key.WorkbookKeys import WorkbookKeys
from com.emeraldblast.p6.proto.P6MsgProtos_pb2 import P6MessageProto, P6ResponseProto
from com.emeraldblast.p6.proto.WorkbookProtos_pb2 import CreateNewWorksheetResponseProto
from com.emeraldblast.p6.proto.WorksheetProtos_pb2 import RenameWorksheetResponseProto


class IntegrationTest_test(unittest.TestCase):
    """ this class includes re-creation of actual bugs """

    def setUp(self) -> None:
        super().setUp()
        # k, z to prevent auto formatting tools from removing the respective imports
        z = WorksheetFunctions
        k = WorkbookKeys
        setIPythonGlobals(globals())
        startApp()
        restartApp()
        getApp().createNewWorkbook("Book1")
        getActiveWorkbook().createNewWorksheet("Sheet1")
        self.wb = getWorkbook("Book1")

    def test_scenario_x(self):
        port = findNewSocketPort()
        zContext = getApp().zContext

        def onReceive(rawMsg):
            msg = P6MessageProto()
            msg.ParseFromString(rawMsg)
            print(msg)

        thread = startREPServerOnThread(True, port, zContext, onReceive)
        socket = self.createSocket(zContext, port)
        getApp().socketProvider.updateREQSocketForUIUpdating(socket)
        s1 = self.wb.getWorksheet("Sheet1")
        s1.cell((1,1)).value = 1
        s1.cell((1,2)).value = 2
        s1.cell((1,3)).formula= "=SUM(A1:A2)"
        s1.cell((1,4)).value= "b"

        sendClose(socket)
        thread.join()


    def test_create_new_workbook(self):
        port = findNewSocketPort()
        zContext = getApp().zContext

        def onReceive(rawMsg):
            msg = P6ResponseProto()
            msg.ParseFromString(rawMsg)
            protoObj = CreateNewWorksheetResponseProto()
            protoObj.ParseFromString(msg.data)
            self.assertEqual("SheetX", protoObj.newWorksheetName)
            print(protoObj)

        thread = startREPServerOnThread(True, port, zContext, onReceive)
        socket = self.createSocket(zContext, port)
        getApp().socketProvider.updateREQSocketForUIUpdating(socket)
        self.wb.createNewWorksheet("SheetX")
        sendClose(socket)
        thread.join()

    def createSocket(self, zContext, port):
        socket = zContext.socket(zmq.REQ)
        socket.connect(f"tcp://localhost:{port}")
        return socket

    def test_bug1(self):
        """bug1: this wb unable to generate json"""
        app = getApp()
        w1 = app.createNewWorkbook("w1")
        s1 = w1.createNewWorksheet("s1")
        c1 = s1.cell("@A1")
        c1.value = 1
        c2 = s1.cell("@A2")
        c2.value = 2
        c3 = s1.cell("@A3")
        c3.formula = """=SUM(A1:A2)"""
        c4 = s1.cell("@A4")
        c4.value = "abc"
        print(c1.value)
        print(c2.value)
        print(c3.value)
        print(c4.value)
        s1.toJsonStr()

    def test_rename(self):
        port = findNewSocketPort()
        context = getApp().zContext

        def onReceive(data):
            msg = P6ResponseProto()
            msg.ParseFromString(data)
            dataObj = RenameWorksheetResponseProto()
            dataObj.ParseFromString(msg.data)
            self.assertEqual("Sheet1", dataObj.oldName)
            self.assertEqual("Sheet1x", dataObj.newName)
            self.assertEqual("Book1", dataObj.workbookKey.name)
            self.assertEqual("null", dataObj.workbookKey.path.WhichOneof("kind"))
            print(dataObj)

        thread = startREPServerOnThread(True, port, context, onReceive)
        book = getWorkbook("Book1")
        socket = self.createSocket(context,port)
        getApp().socketProvider.updateREQSocketForUIUpdating(socket)
        book.getWorksheet("Sheet1").renameRs("Sheet1x")
        sendClose(socket)
        thread.join()

    def test_reaction(self):
        app = getApp()
        port = findNewSocketPort()
        context = getApp().zContext

        def onReceive(data):
            print(data)

        thread = startREPServerOnThread(True, port, context, onReceive)
        socket = self.createSocket(context,port)
        app.socketProvider.updateREQSocketForUIUpdating(socket)

        w1 = app.createNewWorkbook("w1")
        s1 = w1.createNewWorksheet("s1")
        c1 = s1.cell("@A1")
        c1.value = 1
        sendClose(socket)

        thread.join()