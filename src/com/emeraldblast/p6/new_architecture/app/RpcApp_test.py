import unittest
from unittest.mock import MagicMock

from com.emeraldblast.p6.document_structure.util.for_test import TestUtils

from com.emeraldblast.p6.document_structure.workbook.key.WorkbookKeyImp import WorkbookKeyImp
from com.emeraldblast.p6.document_structure.workbook.key.WorkbookKeys import WorkbookKeys
from com.emeraldblast.p6.new_architecture.app.RpcApp import RpcApp
from com.emeraldblast.p6.new_architecture.rpc.data_structure.app.GetWorkbookRequest import GetWorkbookRequest
from com.emeraldblast.p6.new_architecture.rpc.data_structure.app.WorkbookKeyWithErrorResponse import \
    WorkbookKeyWithErrorResponse
from com.emeraldblast.p6.new_architecture.workbook.RpcWorkbook import RpcWorkbook
from com.emeraldblast.p6.proto.rpc.app.GetWorkbookRequestProto_pb2 import GetWorkbookRequestProto


class RpcApp_test(unittest.TestCase):
    def setUp(self) -> None:
        super().setUp()
        mockSP = MagicMock()
        mockWbService = MagicMock()
        mockSP.appService = mockWbService
        self.mockSP = mockSP
        self.appService = mockWbService
        self.app = RpcApp(
            rpcStubProvider = mockSP
        )

    def test_getWorkbookRs(self):
        wbKey = WorkbookKeys.fromNameAndPath("asd")

        def c1():
            self.appService.getWorkbook = MagicMock(return_value = WorkbookKeyWithErrorResponse(
                wbKey = wbKey
            ).toProtoObj())

            rs1 = self.app.getWorkbookRs(1)

            self.appService.getWorkbook.assert_called_with(
                request = GetWorkbookRequest(
                    wbKey = None,
                    wbName = None,
                    wbIndex = 1,
                ).toProtoObj()
            )
            self.assertTrue(rs1.isOk())

            expectWb = RpcWorkbook(wbKey.fileName, wbKey.filePath, self.mockSP)
            self.assertEqual(expectWb, self.app.getWorkbook("asd"))
            self.assertEqual(expectWb, self.app.getWorkbookByKey(wbKey))
            self.assertEqual(expectWb, self.app.getWorkbookByIndex(1))
            self.assertEqual(expectWb, self.app.getWorkbookOrNone(1))

        c1()

        def c2():
            rs2 = self.app.getWorkbookRs("a")

            self.appService.getWorkbook.assert_called_with(
                request = GetWorkbookRequest(
                    wbKey = None,
                    wbName = "a",
                    wbIndex = None,
                ).toProtoObj()
            )

            rs3 = self.app.getWorkbookRs(wbKey)

            self.appService.getWorkbook.assert_called_with(
                request = GetWorkbookRequest(
                    wbKey = wbKey,
                    wbName = None,
                    wbIndex = None,
                ).toProtoObj()
            )

        c2()

        def c3():
            self.appService.getWorkbook = MagicMock(return_value = WorkbookKeyWithErrorResponse(
                wbKey = wbKey, errorReport = TestUtils.TestErrorReport
            ).toProtoObj())

            rs4 = self.app.getWorkbookRs("wbqwe")
            self.assertTrue(rs4.isErr())
            self.assertTrue(rs4.err.isSameErr(TestUtils.TestErrorReport))

            with self.assertRaises(Exception):
                self.app.getWorkbook("asd")
            with self.assertRaises(Exception):
                self.app.getWorkbookByKey(wbKey)
            with self.assertRaises(Exception):
                self.app.getWorkbookByName("asd")
            with self.assertRaises(Exception):
                self.app.getWorkbookByIndex(1)
            self.assertIsNone(self.app.getWorkbookOrNone(1))
        c3()

if __name__ == '__main__':
    unittest.main()
