import unittest
from unittest.mock import MagicMock

from com.qxdzbc.p6.document_structure.communication.event.data_structure.SingleSignalResponse import \
    SingleSignalResponse

from com.qxdzbc.p6.document_structure.util.for_test import TestUtils
from com.qxdzbc.p6.document_structure.workbook.key.WorkbookKeys import WorkbookKeys
from com.qxdzbc.p6.document_structure.worksheet.Worksheet import Worksheet
from com.qxdzbc.p6.document_structure.worksheet.WorksheetImp import WorksheetImp

from com.qxdzbc.p6.new_architecture.rpc.RpcValues import RpcValues
from com.qxdzbc.p6.new_architecture.rpc.data_structure.workbook.AddWorksheetRequest import AddWorksheetRequest
from com.qxdzbc.p6.new_architecture.rpc.data_structure.workbook.GetActiveWorksheetResponse import \
    GetActiveWorksheetResponse
from com.qxdzbc.p6.new_architecture.rpc.data_structure.workbook.GetAllWorksheetsResponse import \
    GetAllWorksheetsResponse
from com.qxdzbc.p6.new_architecture.rpc.data_structure.workbook.GetWorksheetResponse import GetWorksheetResponse
from com.qxdzbc.p6.new_architecture.rpc.data_structure.WorksheetId import WorksheetId
from com.qxdzbc.p6.new_architecture.rpc.data_structure.workbook.WorksheetWithErrorReportMsg import \
    WorksheetWithErrorReportMsg
from com.qxdzbc.p6.new_architecture.workbook.RpcWorkbook import RpcWorkbook
from com.qxdzbc.p6.proto.rpc.workbook.service.WorkbookService_pb2_grpc import WorkbookServiceServicer


class RpcWorkbook_test(unittest.TestCase):
    class WorkbookServicerImp(WorkbookServiceServicer):
        def sheetCount(self, request, context):
            return RpcValues.int64(123)

        def setWbName(self, request, context):
            return SingleSignalResponse().toProtoObj()

    def setUp(self) -> None:
        super().setUp()
        # self.mockServer = MockRpcServer()
        # addWbServicer = partial(
        #     WorkbookService_pb2_grpc.add_WorkbookServiceServicer_to_server,
        #     servicer = RpcWorkbook_test.WorkbookServicerImp()
        # )
        # self.mockServer.addServicer(addWbServicer)
        # self.mockServer.start()
        mockSP = MagicMock()
        mockWbService = MagicMock()
        mockSP.wbService = mockWbService
        self.mockSP = mockSP
        self.mockWbService = mockWbService
        self.wb = RpcWorkbook(
            name = "qwe",
            path = None,
            stubProvider = self.mockSP
        )

    def tearDown(self) -> None:
        # super().tearDown()
        # self.mockServer.stop()
        pass

    def test_sheetCount(self):
        self.mockWbService.sheetCount = MagicMock(return_value = RpcValues.int64(123))
        wb = self.wb
        self.assertEqual(123, wb.sheetCount)

    def test_set_wbKey_ok(self):
        self.mockWbService.setWbKey = MagicMock(
            return_value = SingleSignalResponse().toProtoObj())
        self.wb.workbookKey = WorkbookKeys.fromNameAndPath("newName")
        self.assertEqual("newName", self.wb.name)

    def test_set_wbKey_fail(self):
        self.mockWbService.setWbKey = MagicMock(return_value = SingleSignalResponse(
            errorReport = TestUtils.TestErrorReport
        ).toProtoObj())
        with self.assertRaises(Exception):
            self.wb.workbookKey = WorkbookKeys.fromNameAndPath("newName")
        self.assertEqual("qwe", self.wb.name)

    def test_worksheets(self):
        wsl = [
            WorksheetImp("Sheet1", self.wb),
            WorksheetImp("Sheet2", self.wb),
        ]
        self.mockWbService.getAllWorksheets = MagicMock(return_value = GetAllWorksheetsResponse(
            worksheets = wsl,
            errorReport = None
        ).toProtoObj())
        out: list[Worksheet] = self.wb.worksheets
        self.assertEqual(2, len(self.wb.worksheets))
        self.assertEqual("Sheet1", out[0].name)
        self.assertEqual("Sheet2", out[1].name)

    def test_setActiveWorksheetRs(self):
        wb = self.wb
        rpcCall = MagicMock(
            return_value = SingleSignalResponse(
                errorReport = None
            ).toProtoObj()
        )
        self.mockWbService.setActiveWorksheet =rpcCall

        o1 = wb.setActiveWorksheetRs(123)
        self.assertTrue(o1.isOk())
        rpcCall.assert_called_with(
            request=WorksheetId(
                wbKey=wb.workbookKey,
                wsIndex = 123
            ).toProtoObj()
        )
        o2 = wb.setActiveWorksheetRs("qwe")
        self.assertTrue(o2.isOk())
        rpcCall.assert_called_with(
            request = WorksheetId(
                wbKey = wb.workbookKey,
                wsName = "qwe"
            ).toProtoObj()
        )

        # ====== error case ====== #
        self.mockWbService.setActiveWorksheet = MagicMock(
            return_value = SingleSignalResponse(
                errorReport = TestUtils.TestErrorReport
            ).toProtoObj()
        )

        o3 = wb.setActiveWorksheetRs("asd")
        self.assertTrue(o3.isErr())
        self.assertTrue(o3.err.isSameErr(TestUtils.TestErrorReport))
    
    def test_getActiveWorksheet(self):
        self.mockWbService.getActiveWorksheet = MagicMock(
            return_value = GetActiveWorksheetResponse().toProtoObj()
        )
        wb=self.wb
        o = wb.activeWorksheet
        self.assertIsNone(o)
        self.mockWbService.getActiveWorksheet = MagicMock(
            return_value = GetActiveWorksheetResponse(
                worksheet = WorksheetImp("w",None)
            ).toProtoObj()
        )
        o2 = wb.activeWorksheet
        self.assertIsNotNone(o2)
        self.assertEqual("w",o2.name)

    def test_getWorksheet(self):
        wb = self.wb
        def failTest():
            self.mockWbService.getWorksheet = MagicMock(
                return_value = GetWorksheetResponse().toProtoObj()
            )
            o11 = wb.getWorksheetByNameRs("q")
            self.assertTrue(o11.isErr())

            with self.assertRaises(Exception):
                wb.getWorksheet("q")
            with self.assertRaises(Exception):
                wb.getWorksheetByName("q")
            self.assertIsNone(wb.getWorksheetByNameOrNone("q"))

            o12=wb.getWorksheetRs("q")
            self.assertTrue(o12.isErr())
            self.assertIsNone(wb.getWorksheetOrNone("q"))

            o13 = wb.getWorksheetByIndexRs(123)
            self.assertTrue(o13.isErr())

            with self.assertRaises(Exception):
                wb.getWorksheet(123)
            with self.assertRaises(Exception):
                wb.getWorksheetByIndex(123)
            self.assertIsNone(wb.getWorksheetByIndexOrNone(123))

            o14=wb.getWorksheetRs(123)
            self.assertTrue(o14.isErr())

        failTest()
        def okTest():
            ws2 = WorksheetImp("ws2",None)
            self.mockWbService.getWorksheet = MagicMock(
                return_value = GetWorksheetResponse(
                    worksheet = ws2
                ).toProtoObj()
            )
            o21 = self.wb.getWorksheetByNameRs("q")
            self.assertTrue(o21.isOk())
            self.assertTrue(o21.value.compareContent(ws2))

            self.assertTrue(wb.getWorksheetByName("q").compareContent(ws2))
            self.assertTrue(wb.getWorksheetByNameOrNone("q").compareContent(ws2))
            self.assertTrue(wb.getWorksheetOrNone("q").compareContent(ws2))

            o22 = wb.getWorksheetRs("q")
            self.assertTrue(o22.value.compareContent(ws2))

            o21 = self.wb.getWorksheetByIndexRs(123)
            self.assertTrue(o21.isOk())
            self.assertTrue(o21.value.compareContent(ws2))

            self.assertTrue(wb.getWorksheetByIndex(123).compareContent(ws2))
            self.assertTrue(wb.getWorksheetByIndexOrNone(123).compareContent(ws2))
            self.assertTrue(wb.getWorksheetOrNone(123).compareContent(ws2))

            o22 = wb.getWorksheetRs(123)
            self.assertTrue(o22.value.compareContent(ws2))

        okTest()

    def test_createNewWorksheet(self):
        ws2 = WorksheetImp("ws2", None)
        self.mockWbService.createNewWorksheet = MagicMock(
            return_value = WorksheetWithErrorReportMsg(
                wsName = ws2.name
            ).toProtoObj()
        )
        wb = self.wb
        rs=wb.createNewWorksheetRs("qwe")
        self.assertTrue(rs.isOk())
        self.assertTrue(rs.value.compareContent(ws2))
        self.assertTrue(wb.createNewWorksheet("qwe").compareContent(ws2))


        self.mockWbService.createNewWorksheet = MagicMock(
            return_value = WorksheetWithErrorReportMsg(
                errorReport = TestUtils.TestErrorReport
            ).toProtoObj()
        )
        rs = wb.createNewWorksheetRs("qwe")
        self.assertTrue(rs.isErr())
        with self.assertRaises(Exception):
            wb.createNewWorksheet("qwe")

    def test_deleteWorksheet(self):
        self.mockWbService.deleteWorksheet = MagicMock(
            return_value = SingleSignalResponse().toProtoObj()
        )

        wb = self.wb
        o = wb.deleteWorksheetByNameRs("qwe")
        self.assertTrue(o.isOk())
        o = wb.deleteWorksheetByIndexRs(123)
        self.assertTrue(o.isOk())

        self.mockWbService.deleteWorksheet = MagicMock(
            return_value = SingleSignalResponse(
                errorReport = TestUtils.TestErrorReport
            ).toProtoObj()
        )

        o = wb.deleteWorksheetByNameRs("qwe")
        self.assertTrue(o.isErr())
        self.assertTrue(o.err.isSameErr(TestUtils.TestErrorReport))
        o = wb.deleteWorksheetByIndexRs(123)
        self.assertTrue(o.isErr())
        self.assertTrue(o.err.isSameErr(TestUtils.TestErrorReport))


        with self.assertRaises(Exception):
            wb.deleteWorksheet(123)

        with self.assertRaises(Exception):
            wb.deleteWorksheet("qwe")



    def test_addWorksheet(self):
        self.mockWbService.addWorksheet = MagicMock(
            return_value = SingleSignalResponse().toProtoObj()
        )
        ws = WorksheetImp("zxc",None)
        wb= self.wb
        rs = wb.addWorksheetRs(ws)

        self.mockWbService.addWorksheet.assert_called_with(
            request=AddWorksheetRequest(
                wbKey = wb.workbookKey,
                worksheet = ws
            ).toProtoObj()
        )

        self.assertTrue(rs.isOk())
        wb.addWorksheet(ws)

        self.mockWbService.addWorksheet = MagicMock(
            return_value = SingleSignalResponse(
                errorReport = TestUtils.TestErrorReport
            ).toProtoObj()
        )
        rs = wb.addWorksheetRs(ws)
        self.assertTrue(rs.isErr())
        with self.assertRaises(Exception):
            wb.addWorksheet(ws)




if __name__ == '__main__':
    unittest.main()