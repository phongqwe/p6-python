import time
import unittest

import zmq

# these 2 imports must be keep for the formula script to be able to run
from com.emeraldblast.p6.document_structure.app.UserFunctions import *
from com.emeraldblast.p6.document_structure.cell.address.CellAddresses import CellAddresses
from com.emeraldblast.p6.document_structure.communication.event.P6Events import P6Events
from com.emeraldblast.p6.document_structure.communication.event.data_structure.cell_event.CellUpdateRequest import \
    CellUpdateRequest
from com.emeraldblast.p6.document_structure.communication.event_server.response.P6Response import P6Response
from com.emeraldblast.p6.document_structure.util.for_test.TestUtils import findNewSocketPort, startREPServerOnThread, \
    sendClose
from com.emeraldblast.p6.document_structure.util.for_test.emu.TestEnvImp import TestEnvImp
from com.emeraldblast.p6.document_structure.workbook.key.WorkbookKeys import WorkbookKeys
from com.emeraldblast.p6.proto.P6MsgProtos_pb2 import P6MessageProto, P6ResponseProto, P6MessageHeaderProto
from com.emeraldblast.p6.proto.WorkbookProtos_pb2 import CreateNewWorksheetResponseProto, SaveWorkbookRequestProto
from com.emeraldblast.p6.proto.WorksheetProtos_pb2 import RenameWorksheetResponseProto


class IntegrationTest_test(unittest.TestCase):
    """ this class includes re-creation of actual bugs. These tests are not run with other test because it slows down other tests """

    def setUp(self) -> None:
        super().setUp()
        self.testEnv = TestEnvImp()
        self.testEnv.startApp()
        self.wb = self.testEnv.app.getWorkbook("Book1")
        self.z = False
        self.testEnv.createNotifSender()

    def tearDown(self) -> None:
        self.testEnv.stopAll()

    def test_bug3(self):
        def onReceive(rawMsg):
            msg = P6MessageProto()
            msg.ParseFromString(rawMsg)
            print(msg)
            self.z = True

        self.testEnv.startNotificationListenerOnThread(True, onReceive)
        wb = self.testEnv.app.getWorkbook("Book1")
        saveReq = P6MessageProto(
            header = P6MessageHeaderProto(
                msgId = "1",
                eventType = P6Events.Workbook.SaveWorkbook.event.toProtoObj()
            ),
            data = SaveWorkbookRequestProto(
                workbookKey = wb.workbookKey.toProtoObj(),
                path = "/home/abc/MyTemp/b1.txt"
            ).SerializeToString()
        )

        zsocket = self.testEnv.requestZSocket
        zsocket.send(saveReq.SerializeToString())

        rec = zsocket.recv()
        saveResProto = P6ResponseProto()
        saveResProto.ParseFromString(rec)
        saveRes = P6Response.fromProto(saveResProto)

        self.assertTrue(saveRes.status == P6Response.Status.OK)

        cellUpdateRequest = P6MessageProto(
            header = P6MessageHeaderProto(
                msgId = "2",
                eventType = P6Events.Cell.Update.event.toProtoObj()
            ),
            data = CellUpdateRequest(
                workbookKey = WorkbookKeys.fromNameAndPath(
                    "b1.txt",
                    "/home/abc/MyTemp/b1.txt",
                ),
                worksheetName = "Sheet1",
                cellAddress = CellAddresses.fromLabel("@C1"),
                value = "321",
                formula = None
            ).toProtoObj().SerializeToString()
        )

        zsocket.send(cellUpdateRequest.SerializeToString())
        r = zsocket.recv()
        cellUpdateResProto = P6ResponseProto()
        cellUpdateResProto.ParseFromString(r)
        cellUpdateRes = P6Response.fromProto(cellUpdateResProto)
        self.assertEqual(P6Response.Status.OK, cellUpdateRes.status)
        print(wb.getWorksheet("Sheet1").cell("@C1").value)

    def test_scenario_changeUpdateCell(self):
        wb = self.testEnv.app.getWorkbook("Book1")
        self.z = False

        def onReceive(rawMsg):
            msg = P6MessageProto()
            msg.ParseFromString(rawMsg)
            print(msg)
            self.z = True

        self.testEnv.startNotificationListenerOnThread(True, onReceive)
        s1 = wb.getWorksheet("Sheet1")
        s1.cell((1, 1)).value = 1
        s1.cell((1, 2)).value = 2
        s1.cell((1, 3)).formula = "=SUM(A1:A2)"
        s1.cell((1, 4)).value = "b"
        self.assertTrue(self.z)

    def test_create_new_workbook(self):
        def onReceive(rawMsg):
            msg = P6ResponseProto()
            msg.ParseFromString(rawMsg)
            print(msg)
            protoObj = CreateNewWorksheetResponseProto()
            protoObj.ParseFromString(msg.data)
            self.assertEqual("SheetX", protoObj.newWorksheetName)
            print(protoObj)

        self.testEnv.startNotificationListenerOnThread(True, onReceive)
        self.wb.createNewWorksheet("SheetX")

    def createSocket(self, zContext, port):
        socket = zContext.socket(zmq.REQ)
        socket.connect(f"tcp://localhost:{port}")
        return socket

    def test_bug1(self):
        """bug1: this wb unable to generate json"""
        self.testEnv.removeNotifSender()
        app = self.testEnv.app
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
        context = self.testEnv.app.zContext

        def onReceive(data):
            msg = P6ResponseProto()
            msg.ParseFromString(data)
            dataObj = RenameWorksheetResponseProto()
            dataObj.ParseFromString(msg.data)
            self.assertEqual("Sheet1", dataObj.oldName)
            self.assertEqual("Sheet1x", dataObj.newName)
            self.assertEqual("Book1", dataObj.workbookKey.name)
            self.assertFalse(dataObj.workbookKey.HasField("path"))
            print(dataObj)

        thread = startREPServerOnThread(True, port, context, onReceive)
        book = getWorkbook("Book1")
        socket = self.createSocket(context, port)
        self.testEnv.app.socketProvider.updateREQSocketForUIUpdating(socket)
        book.getWorksheet("Sheet1").renameRs("Sheet1x")

    def test_reaction(self):
        app = self.testEnv.app

        def onReceive(data):
            print(data)

        self.testEnv.startNotificationListenerOnThread(True, onReceive)

        w1 = app.createNewWorkbook("w1")
        s1 = w1.createNewWorksheet("s1")
        c1 = s1.cell("@A1")
        c1.value = 1
