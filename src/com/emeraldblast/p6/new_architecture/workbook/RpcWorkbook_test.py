import unittest
from functools import partial
from unittest.mock import MagicMock

import grpc
from com.emeraldblast.p6.document_structure.communication.event.data_structure.SingleSignalResponse import \
    SingleSignalResponse

from com.emeraldblast.p6.document_structure.util.for_test import TestUtils
from com.emeraldblast.p6.document_structure.worksheet.WorksheetImp import WorksheetImp

from com.emeraldblast.p6.new_architecture.rpc.InsecureStubProvider import InsecureStubProvider
from com.emeraldblast.p6.new_architecture.rpc.RpcInfo import RpcInfo
from com.emeraldblast.p6.new_architecture.rpc.RpcValues import RpcValues
from com.emeraldblast.p6.new_architecture.rpc.data_structure.workbook.GetAllWorksheetsResponse import \
    GetAllWorksheetsResponse
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
        self.assertEqual(2, len(self.wb.worksheets))
        # self.assertEqual(wsl, self.wb.worksheets)


if __name__ == '__main__':
    unittest.main()
