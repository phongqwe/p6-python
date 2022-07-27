import unittest
from functools import partial

import grpc

from com.emeraldblast.p6.new_architecture.rpc.InsecureStubProvider import InsecureStubProvider
from com.emeraldblast.p6.new_architecture.rpc.RpcInfo import RpcInfo
from com.emeraldblast.p6.new_architecture.rpc.RpcValues import RpcValues
from com.emeraldblast.p6.new_architecture.rpc.for_test.mock_rpc_server.MockRpcServer import MockRpcServer
from com.emeraldblast.p6.new_architecture.workbook.RpcWorkbook import RpcWorkbook
from com.emeraldblast.p6.proto.service.workbook import WorkbookService_pb2_grpc
from com.emeraldblast.p6.proto.service.workbook.WorkbookService_pb2 import Empty2
from com.emeraldblast.p6.proto.service.workbook.WorkbookService_pb2_grpc import WorkbookServiceStub, \
    WorkbookServiceServicer


class RpcWorkbook_test(unittest.TestCase):
    class WorkbookServicerImp(WorkbookServiceServicer):
        def sheetCount(self, request, context):
            return RpcValues.int64(123)

    def setUp(self) -> None:
        super().setUp()
        self.mockServer = MockRpcServer()
        addWbServicer = partial(
            WorkbookService_pb2_grpc.add_WorkbookServiceServicer_to_server,
            servicer = RpcWorkbook_test.WorkbookServicerImp()
        )
        self.mockServer.addServicer(addWbServicer)
        self.mockServer.start()

    def tearDown(self) -> None:
        super().tearDown()
        self.mockServer.stop()

    def test_sheetCount(self):
        wb = RpcWorkbook(
            name = "qwe",
            path = None,
            stubProvider = MockRpcServer.stubProvider
        )
        self.assertEqual(123, wb.sheetCount)


if __name__ == '__main__':
    unittest.main()
