import unittest
from functools import partial
from unittest.mock import MagicMock

import grpc
from com.emeraldblast.p6.document_structure.util.for_test import TestUtils

from com.emeraldblast.p6.new_architecture.rpc.InsecureStubProvider import InsecureStubProvider
from com.emeraldblast.p6.new_architecture.rpc.RpcInfo import RpcInfo
from com.emeraldblast.p6.new_architecture.rpc.RpcValues import RpcValues
from com.emeraldblast.p6.new_architecture.rpc.data_structure.workbook.SetWbName import SetWbNameResponse
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
            return SetWbNameResponse().toProtoObj()

    def setUp(self) -> None:
        super().setUp()
        self.mockServer = MockRpcServer()
        addWbServicer = partial(
            WorkbookService_pb2_grpc.add_WorkbookServiceServicer_to_server,
            servicer = RpcWorkbook_test.WorkbookServicerImp()
        )
        self.mockServer.addServicer(addWbServicer)
        self.mockServer.start()
        self.wb = RpcWorkbook(
            name = "qwe",
            path = None,
            stubProvider = MockRpcServer.stubProvider
        )
        mockSP = MagicMock()
        mockWbService = MagicMock()
        mockSP.wbService = mockWbService
        self.mockSP = mockSP
        self.mockWbService = mockWbService

    def tearDown(self) -> None:
        super().tearDown()
        self.mockServer.stop()

    def test_sheetCount(self):
        wb = self.wb
        self.assertEqual(123, wb.sheetCount)

    def test_set_name_ok(self):
        self.mockWbService.setWbName = MagicMock(return_value=SetWbNameResponse().toProtoObj())
        self.wb.setStubProvider(self.mockSP)
        self.wb.name = "newName"
        self.assertEqual("newName",self.wb.name)

    def test_set_name_fail(self):
        self.mockWbService.setWbName = MagicMock(return_value=SetWbNameResponse(
            errorReport = TestUtils.TestErrorReport
        ).toProtoObj())
        self.wb.setStubProvider(self.mockSP)
        with self.assertRaises(Exception):
            self.wb.name = "newName"
        self.assertEqual("qwe",self.wb.name)




if __name__ == '__main__':
    unittest.main()
