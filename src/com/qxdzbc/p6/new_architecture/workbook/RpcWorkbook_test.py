import unittest
from unittest.mock import MagicMock


from com.qxdzbc.p6.document_structure.util.for_test import TestUtils
from com.qxdzbc.p6.document_structure.workbook.key.WorkbookKeys import WorkbookKeys
from com.qxdzbc.p6.document_structure.worksheet.Worksheet import Worksheet
from com.qxdzbc.p6.new_architecture.rpc.RpcValues import RpcValues
from com.qxdzbc.p6.new_architecture.rpc.data_structure.SingleSignalResponse import \
    SingleSignalResponse
from com.qxdzbc.p6.new_architecture.rpc.data_structure.worksheet.WorksheetId import WorksheetId
from com.qxdzbc.p6.new_architecture.rpc.data_structure.workbook.AddWorksheetRequest import AddWorksheetRequest
from com.qxdzbc.p6.new_architecture.rpc.data_structure.workbook.GetAllWorksheetsResponse import \
    GetAllWorksheetsResponse
from com.qxdzbc.p6.new_architecture.rpc.data_structure.workbook.GetWorksheetResponse import GetWorksheetResponse
from com.qxdzbc.p6.new_architecture.rpc.data_structure.workbook.WorksheetWithErrorReportMsg import \
    WorksheetWithErrorReportMsg
from com.qxdzbc.p6.new_architecture.rpc.data_structure.worksheet.WorksheetIdWithIndex import WorksheetIdWithIndex
from com.qxdzbc.p6.new_architecture.workbook.RpcWorkbook import RpcWorkbook
from com.qxdzbc.p6.new_architecture.worksheet.RpcWorksheet import RpcWorksheet


class RpcWorkbook_test(unittest.TestCase):

    def setUp(self) -> None:
        super().setUp()
        mockSP = MagicMock()
        mockWbService = MagicMock()
        mockSP.wbService = mockWbService
        self.mockSP = mockSP
        self.mockWbService = mockWbService
        self.wb = RpcWorkbook.fromNameAndPath(
            name = "qwe",
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
            RpcWorksheet("Sheet1", self.wb.workbookKey,self.mockSP),
            RpcWorksheet("Sheet2", self.wb.workbookKey,self.mockSP),
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
            request=WorksheetIdWithIndex(
                wbKey=wb.workbookKey,
                wsIndex = 123
            ).toProtoObj()
        )
        o2 = wb.setActiveWorksheetRs("qwe")
        self.assertTrue(o2.isOk())
        rpcCall.assert_called_with(
            request = WorksheetIdWithIndex(
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
            return_value = GetWorksheetResponse().toProtoObj()
        )
        wb=self.wb
        o = wb.activeWorksheet
        self.assertIsNone(o)
        self.mockWbService.getActiveWorksheet = MagicMock(
            return_value = GetWorksheetResponse(
                wsId = RpcWorksheet("w",self.wb.workbookKey,self.mockSP).id
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
        def okTest():
            ws2 = RpcWorksheet("ws2", self.wb.workbookKey, self.mockSP)
            self.mockWbService.getWorksheet = MagicMock(
                return_value = GetWorksheetResponse(
                    wsId = ws2.id
                ).toProtoObj()
            )
            o21 = self.wb.getWorksheetByNameRs("q")
            self.assertTrue(o21.isOk())
            self.assertTrue(o21.value == ws2.id)

            self.assertEqual(wb.getWorksheetByName("q"), ws2.id)
            self.assertEqual(wb.getWorksheetByNameOrNone("q"), ws2.id)
            self.assertEqual(wb.getWorksheetOrNone("q"), ws2.id)

            o22 = wb.getWorksheetRs("q")
            self.assertEqual(o22.value, ws2.id)

            o21 = self.wb.getWorksheetByIndexRs(123)
            self.assertTrue(o21.isOk())
            self.assertEqual(o21.value, ws2.id)

            self.assertEqual(wb.getWorksheetByIndex(123), ws2.id)
            self.assertEqual(wb.getWorksheetByIndexOrNone(123), ws2.id)
            self.assertEqual(wb.getWorksheetOrNone(123), ws2.id)

            o22 = wb.getWorksheetRs(123)
            self.assertEqual(o22.value, ws2.id)
        failTest()
        okTest()

    def test_createNewWorksheet(self):
        ws2 = RpcWorksheet("ws2", self.wb.workbookKey, self.mockSP)
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
        ws = RpcWorksheet("qwe", self.wb.workbookKey, self.mockSP)
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
