import unittest
from unittest.mock import MagicMock

from com.qxdzbc.p6.util.for_test import TestUtils
from com.qxdzbc.p6.workbook.key.WorkbookKeys import WorkbookKeys
from com.qxdzbc.p6.app.RpcApp import RpcApp
from com.qxdzbc.p6.rpc.data_structure.BoolMsg import BoolMsg
from com.qxdzbc.p6.rpc.data_structure.SingleSignalResponse import SingleSignalResponse
from com.qxdzbc.p6.app.rpc_data_structure.GetAllWorkbookResponse import GetAllWorkbookResponse
from com.qxdzbc.p6.app.rpc_data_structure.LoadWorkbookResponse import LoadWorkbookResponse
from com.qxdzbc.p6.workbook.rpc_data_structure.save_wb.SaveWorkbookRequest import SaveWorkbookRequest
from com.qxdzbc.p6.workbook.rpc_data_structure.save_wb.SaveWorkbookResponse import SaveWorkbookResponse
from com.qxdzbc.p6.worksheet.rpc_data_structure.WorksheetId import WorksheetId
from com.qxdzbc.p6.app.rpc_data_structure.CreateNewWorkbookRequest import CreateNewWorkbookRequest
from com.qxdzbc.p6.app.rpc_data_structure.CreateNewWorkbookResponse import CreateNewWorkbookResponse
from com.qxdzbc.p6.app.rpc_data_structure.GetWorkbookRequest import GetWorkbookRequest
from com.qxdzbc.p6.app.rpc_data_structure.WorkbookKeyWithErrorResponse import \
    WorkbookKeyWithErrorResponse
from com.qxdzbc.p6.workbook.rpc_data_structure.GetWorksheetResponse import GetWorksheetResponse
from com.qxdzbc.p6.workbook.RpcWorkbook import RpcWorkbook
from com.qxdzbc.p6.proto.CommonProtos_pb2 import EmptyProto



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
        self.wbk = WorkbookKeys.fromNameAndPath("wb1")

    def test_workbooks(self):
        self.appService.getAllWorkbooks = MagicMock(
            return_value = GetAllWorkbookResponse().toProtoObj()
        )
        o = self.app.workbooks
        self.assertEqual(0,len(o))

        wbks = list(map(lambda n: WorkbookKeys.fromNameAndPath(n),["wb1","wb2"]))
        self.appService.getAllWorkbooks = MagicMock(
            return_value = GetAllWorkbookResponse(wbks).toProtoObj()
        )
        o = self.app.workbooks
        self.assertEqual(2,len(o))
        self.assertEqual(
            wbks, list(map(lambda wb: wb.key, o))
        )


    def test_hasWorkbook(self):
        wbk = self.wbk
        self.appService.checkWbExistence = MagicMock(
            return_value = BoolMsg(True).toProtoObj()
        )
        o = self.app.hasWorkbook(wbk)
        self.assertTrue(o)

    def test_loadWb(self):
        wbk = self.wbk
        p = "some/path"
        def okCase():
            self.appService.loadWorkbook = MagicMock(
                return_value = LoadWorkbookResponse(
                    wbKey = wbk
                ).toProtoObj()
            )
            o = self.app.loadWorkbookRs(p)
            self.assertTrue(o.isOk())
            self.app.loadWorkbook(p)
        def errCase():
            self.appService.loadWorkbook = MagicMock(
                return_value = LoadWorkbookResponse(
                    errorReport = TestUtils.TestErrorReport
                ).toProtoObj()
            )
            o = self.app.loadWorkbookRs(p)
            self.assertTrue(o.isErr())
            with self.assertRaises(Exception):
                self.app.loadWorkbook(p)
        okCase()
        errCase()
    def test_closeWb(self):
        wbk = WorkbookKeys.fromNameAndPath("wb1")
        def okCase():
            self.appService.closeWorkbook = MagicMock(
                return_value = SingleSignalResponse().toProtoObj()
            )
            o = self.app.closeWorkbookByWbKeyRs(wbKey = wbk)
            self.assertTrue(o.isOk())
            self.app.closeWorkbookByWbKey(wbk)
        def errCase():
            self.appService.closeWorkbook = MagicMock(
                return_value = SingleSignalResponse(
                    TestUtils.TestErrorReport
                ).toProtoObj()
            )
            o = self.app.closeWorkbookByWbKeyRs(wbKey = wbk)
            self.assertTrue(o.isErr())
            with self.assertRaises(Exception):
                self.app.closeWorkbookByWbKey(wbk)
        okCase()
        errCase()

    def test_saveWorkbookAtPath(self):
        wbk = WorkbookKeys.fromNameAndPath("wb1")
        path = "some/path"
        def okCase():
            self.appService.saveWorkbookAtPath = MagicMock(
                return_value = SaveWorkbookResponse(
                    path=path,
                    wbKey = wbk
                ).toProtoObj()
            )
            o = self.app.saveWorkbookAtPathRs(wbKey = wbk,filePath = path)
            self.assertTrue(o.isOk())
            self.appService.saveWorkbookAtPath.assert_called_with(
                request= SaveWorkbookRequest(wbKey = wbk,path=path).toProtoObj()
            )
            self.app.saveWorkbookAtPath(wbKey = wbk,filePath = path)
            o = self.app.saveWorkbookRs(wbKey = wbk)
            self.assertTrue(o.isOk())

        # Error case
        def errorCase():
            self.appService.saveWorkbookAtPath = MagicMock(
                return_value = SaveWorkbookResponse(
                    errorReport = TestUtils.TestErrorReport,
                    path = path
                ).toProtoObj()
            )
            o = self.app.saveWorkbookAtPathRs(wbKey = wbk, filePath = path)
            self.assertTrue(o.isErr())
            o = self.app.saveWorkbookRs(wbKey = wbk)
            self.assertTrue(o.isErr())
            with self.assertRaises(Exception):
                self.app.saveWorkbookAtPath(wbKey = wbk, filePath = path)
            with self.assertRaises(Exception):
                self.app.saveWorkbook(wbKey = wbk)
        okCase()
        errorCase()

    def test_activeWorksheet(self):
        wbk = WorkbookKeys.fromNameAndPath("wb1")
        wsId = WorksheetId(
            wbKey = wbk,
            wsName = "wsname"
        )
        self.appService.getActiveWorksheet = MagicMock(
            return_value = GetWorksheetResponse(
                wsId = wsId
            ).toProtoObj()
        )
        o = self.app.activeWorksheet
        self.appService.getActiveWorksheet.assert_called_with(
            request=EmptyProto()
        )
        self.assertEqual(o.id,wsId)

    def test_setActiveWorkbookRs(self):
        wbk = WorkbookKeys.fromNameAndPath("wb1")
        self.appService.setActiveWorkbook = MagicMock(
            return_value = SingleSignalResponse().toProtoObj()
        )
        o = self.app.setActiveWorkbookRs(wbk)
        self.appService.setActiveWorkbook.assert_called_with(
            request=wbk.toProtoObj()
        )
        self.assertTrue(o.isOk())
        self.assertEqual(RpcWorkbook(wbKey = wbk),o.value)
        self.assertEqual(RpcWorkbook(wbKey = wbk),self.app.setActiveWorkbook(wbk))

        # Error case

        self.appService.setActiveWorkbook = MagicMock(
            return_value = SingleSignalResponse(
                TestUtils.TestErrorReport
            ).toProtoObj()
        )
        o = self.app.setActiveWorkbookRs(wbk)
        self.assertTrue(o.isErr())
        with self.assertRaises(Exception):
            self.app.setActiveWorkbook(wbk)



    def test_getActiveWorkbook(self):
        self.appService.getActiveWorkbook = MagicMock(return_value = WorkbookKeyWithErrorResponse(
            wbKey = WorkbookKeys.fromNameAndPath("qwe")
        ).toProtoObj())

        wb = self.app.activeWorkbook
        self.appService.getActiveWorkbook.assert_called_with(
            request = EmptyProto()
        )
        self.assertTrue(wb is not None)
        self.assertEqual(RpcWorkbook.fromNameAndPath(name = "qwe"), wb)

        # Error case

        self.appService.getActiveWorkbook = MagicMock(return_value = WorkbookKeyWithErrorResponse(
            errorReport = TestUtils.TestErrorReport
        ).toProtoObj())

        wb = self.app.activeWorkbook
        self.assertTrue(wb is None)

    def test_createNewWb(self):
        self.appService.createNewWorkbook = MagicMock(return_value = CreateNewWorkbookResponse(
            wbKey = WorkbookKeys.fromNameAndPath("qwe")
        ).toProtoObj())

        rs1 = self.app.createNewWorkbookRs("qwe")
        self.appService.createNewWorkbook.assert_called_with(
            request=CreateNewWorkbookRequest(
                workbookName = "qwe"
            ).toProtoObj()
        )
        self.assertTrue(rs1.isOk())
        self.assertEqual(RpcWorkbook.fromNameAndPath(name="qwe"),rs1.value)

        self.appService.createNewWorkbook = MagicMock(return_value = CreateNewWorkbookResponse(
            errorReport = TestUtils.TestErrorReport
        ).toProtoObj())
        rs2 = self.app.createNewWorkbookRs("qwe")
        self.assertTrue(rs2.isErr())

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

            expectWb = RpcWorkbook(wbKey, self.mockSP)
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
