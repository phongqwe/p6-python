import time
import unittest

import zmq

# these 2 imports must be keep for the formula script to be able to run
from com.emeraldblast.p6.document_structure.communication.event.data_structure.range_event.RangeId import RangeId
from com.emeraldblast.p6.document_structure.communication.event.data_structure.range_event.range_to_clipboard.RangeToClipboardResponse import \
    RangeToClipboardResponse
from com.emeraldblast.p6.document_structure.communication.event_server.P6Messages import P6Messages
from com.emeraldblast.p6.document_structure.range.address.RangeAddresses import RangeAddresses
from com.emeraldblast.p6.proto.AppEventProtos_pb2 import CreateNewWorkbookResponseProto, CloseWorkbookResponseProto

from com.emeraldblast.p6.document_structure.communication.event.data_structure.app_event.CreateNewWorkbookResponse import \
    CreateNewWorkbookResponse

from com.emeraldblast.p6.document_structure.app.TopLevel import *
from com.emeraldblast.p6.document_structure.cell.address.CellAddresses import CellAddresses
from com.emeraldblast.p6.document_structure.communication.event.P6Events import P6Events
from com.emeraldblast.p6.document_structure.communication.event.data_structure.cell_event.CellUpdateRequest import \
    CellUpdateRequest
from com.emeraldblast.p6.document_structure.communication.event_server.response.P6Response import P6Response
from com.emeraldblast.p6.document_structure.communication.reactor.EventReactors import EventReactors
from com.emeraldblast.p6.document_structure.util.for_test.TestUtils import findNewSocketPort, startREPServerOnThread, \
    sendClose
from com.emeraldblast.p6.document_structure.util.for_test.emu.TestEnvImp import TestEnvImp
from com.emeraldblast.p6.document_structure.workbook.key.WorkbookKeys import WorkbookKeys
from com.emeraldblast.p6.proto.P6MsgProtos_pb2 import P6MessageProto, P6ResponseProto, P6MessageHeaderProto
from com.emeraldblast.p6.proto.RangeProtos_pb2 import RangeToClipboardResponseProto, RangeToClipboardRequestProto
from com.emeraldblast.p6.proto.WorkbookProtos_pb2 import CreateNewWorksheetResponseProto, SaveWorkbookRequestProto
from com.emeraldblast.p6.proto.WorksheetProtos_pb2 import RenameWorksheetResponseProto


class IntegrationTest_test(unittest.TestCase):
    """ this class includes re-creation of actual bugs. These tests are not run with other test because it slows down other tests """

    def setUp(self) -> None:
        super().setUp()
        self.testEnv = TestEnvImp()
        self.testEnv.startEnv()
        self.wb = self.testEnv.app.getWorkbook("Book1")
        self.z = False

    def tearDown(self) -> None:
        self.testEnv.stopAll()

    def test_bug3(self):
        """
        send save wb request to event-server
        """
        wb = self.testEnv.app.getWorkbook("Book1")
        saveReq = P6MessageProto(
            header = P6MessageHeaderProto(
                msgId = "1",
                eventType = P6Events.App.SaveWorkbook.event.toProtoObj()
            ),
            data = SaveWorkbookRequestProto(
                workbookKey = wb.workbookKey.toProtoObj(),
                path = "/home/abc/MyTemp/b1.txt"
            ).SerializeToString()
        )

        rec = self.testEnv.sendRequestToEventServer(saveReq.SerializeToString())
        print(rec.toProtoObj())


    def test_scenario_changeUpdateCell(self):
        """
        send cell update notification to UI
        :return:
        """
        wb = self.testEnv.app.getWorkbook("Book1")
        self.z = False

        s1 = wb.getWorksheet("Sheet1")
        s1.cell((1, 1)).value = 1
        s1.cell((1, 2)).value = 2
        s1.cell((1, 3)).formula = "=SUM(A1:A2)"
        s1.cell((1, 4)).value = "b"

    def test_create_new_worksheet_notification(self):
        """
        send create new worksheet notification to UI
        """

        def onReceive(data):
            protoObj = CreateNewWorksheetResponseProto()
            protoObj.ParseFromString(data)
            self.assertEqual("SheetX", protoObj.newWorksheetName)
            print(protoObj.newWorksheetName)

        self.testEnv.notifListener.addReactor(
            P6Events.Workbook.CreateNewWorksheet.event,
            EventReactors.makeBasicReactor(onReceive))

        self.wb.createNewWorksheet("SheetX")


    def test_rename(self):

        def onReceive(data):
            dataObj = RenameWorksheetResponseProto()
            dataObj.ParseFromString(data)
            self.assertEqual("Sheet1", dataObj.oldName)
            self.assertEqual("Sheet1x", dataObj.newName)
            self.assertEqual("Book1", dataObj.workbookKey.name)
            self.assertFalse(dataObj.workbookKey.HasField("path"))
            print(dataObj)

        self.testEnv.notifListener.addReactor(P6Events.Worksheet.Rename.event,EventReactors.makeBasicReactor(onReceive))
        book = getWorkbook("Book1")
        book.getWorksheet("Sheet1").renameRs("Sheet1x")

    def test_reaction(self):
        app = self.testEnv.app
        w1 = app.createNewWorkbook("w1")
        s1 = w1.createNewWorksheet("s1")
        c1 = s1.cell("@A1")
        c1.value = 1

    def test_updateCellInInvalidWB(self):
        app = self.testEnv.app
        request = CellUpdateRequest(
            workbookKey = WorkbookKeys.fromNameAndPath("InvalidWB"),
            worksheetName = "Sheet1",
            cellAddress = CellAddresses.fromRowCol(1, 1),
            value = "123", formula = ""
        )
        p6Req=P6MessageProto(
            header = P6MessageHeaderProto(
                msgId = "1",
                eventType = P6Events.Cell.Update.event.toProtoObj()
            ),
            data = request.toProtoBytes()
        )
        o = self.testEnv.sendRequestToEventServer(p6Req.SerializeToString())
        print(o)

    def test_check_createNewWB(self):

        def cb(data:bytes):
            proto = CreateNewWorkbookResponseProto()
            proto.ParseFromString(data)
            print(proto)

        self.testEnv.notifListener.addReactorCB(P6Events.App.CreateNewWorkbook.event,cb)

        rs = getApp().createDefaultNewWorkbookRs()
        self.assertTrue(rs.isOk())


    def test_checkCloseWb(self):
        def cb(data:bytes):
            proto = CloseWorkbookResponseProto()
            proto.ParseFromString(data)
            print(proto)
            print("QWE")

        self.testEnv.notifListener.addReactorCB(P6Events.App.CloseWorkbook.event,cb)

        rs = getApp().closeWorkbookRs(0)
        self.assertTrue(rs.isOk())

    def test_rangeToClipboard_eventServer(self):
        res:P6Response = self.testEnv.sendRequestToEventServer(
            P6Messages.p6Message(
                P6Events.Range.RangeToClipBoard.event,
                data=RangeToClipboardRequestProto(
                    rangeId = RangeId(
                        workbookKey = WorkbookKeys.fromNameAndPath("Book1"),
                        worksheetName = "Sheet1",
                        rangeAddress = RangeAddresses.fromLabel("@C1:K5")
                    ).toProtoObj(),
                    windowId = "123"
                ).SerializeToString()
            )
        )
        self.assertEqual(P6Response.Status.OK,res.status)
        proto = RangeToClipboardResponseProto()
        proto.ParseFromString(res.data)
        # print(proto)
        print(proto.errorIndicator)