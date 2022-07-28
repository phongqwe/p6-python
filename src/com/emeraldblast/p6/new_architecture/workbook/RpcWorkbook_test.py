import unittest
from functools import partial
from unittest.mock import MagicMock

import grpc
from com.emeraldblast.p6.document_structure.communication.event.data_structure.SingleSignalResponse import \
    SingleSignalResponse

from com.emeraldblast.p6.document_structure.util.for_test import TestUtils
from com.emeraldblast.p6.document_structure.worksheet.Worksheet import Worksheet
from com.emeraldblast.p6.document_structure.worksheet.WorksheetImp import WorksheetImp

from com.emeraldblast.p6.new_architecture.rpc.InsecureStubProvider import InsecureRpcServiceProvider
from com.emeraldblast.p6.new_architecture.rpc.RpcInfo import RpcInfo
from com.emeraldblast.p6.new_architecture.rpc.RpcValues import RpcValues
from com.emeraldblast.p6.new_architecture.rpc.data_structure.workbook.GetActiveWorksheetResponse import \
    GetActiveWorksheetResponse
from com.emeraldblast.p6.new_architecture.rpc.data_structure.workbook.GetAllWorksheetsResponse import \
    GetAllWorksheetsResponse
from com.emeraldblast.p6.new_architecture.rpc.data_structure.workbook.GetWorksheetResponse import GetWorksheetResponse
from com.emeraldblast.p6.new_architecture.rpc.for_test.mock_rpc_server.MockRpcServer import MockRpcServer
from com.emeraldblast.p6.new_architecture.workbook.RpcWorkbook import RpcWorkbook
from com.emeraldblast.p6.proto.service.workbook import WorkbookService_pb2_grpc
from com.emeraldblast.p6.proto.service.workbook.WorkbookService_pb2_grpc import WorkbookServiceStub, \
    WorkbookServiceServicer


class RpcWorkbook_test(unittest.TestCase):
    class WorkbookServicerImp(WorkbookServiceServicer):
        def sheetCount(self, request, context):
            return RpcValues.int64(123)

        def setWbName(self, request, context):
            return SingleSignalResponse().toProtoObj()

    def setUp(self) -> None:
        super().setUp()
        self.mockServer = MockRpcServer()
        addWbServicer = partial(
            WorkbookService_pb2_grpc.add_WorkbookServiceServicer_to_server,
            servicer = RpcWorkbook_test.WorkbookServicerImp()
        )
        self.mockServer.addServicer(addWbServicer)
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

    def test_set_name_ok(self):
        self.mockWbService.setWbName = MagicMock(return_value = SingleSignalResponse().toProtoObj())
        self.wb.name = "newName"
        self.assertEqual("newName", self.wb.name)

    def test_set_name_fail(self):
        self.mockWbService.setWbName = MagicMock(return_value = SingleSignalResponse(
            errorReport = TestUtils.TestErrorReport
        ).toProtoObj())
        with self.assertRaises(Exception):
            self.wb.name = "newName"
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
        self.mockWbService.setActiveWorksheetRs = MagicMock(
            return_value = SingleSignalResponse(
                errorReport = None
            ).toProtoObj()
        )

        o1 = wb.setActiveWorksheetRs(123)
        self.assertTrue(o1.isOk())
        o2 = wb.setActiveWorksheetRs("qwe")
        self.assertTrue(o2.isOk())

        self.mockWbService.setActiveWorksheetRs = MagicMock(
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




if __name__ == '__main__':
    unittest.main()
