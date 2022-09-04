import unittest

from com.qxdzbc.p6.document_structure.app.errors.AppErrors import AppErrors
from com.qxdzbc.p6.document_structure.cell.address.CellAddresses import CellAddresses
from com.qxdzbc.p6.document_structure.communication.event.data_structure.worksheet_event.DeleteMultiResponse import \
    DeleteMultiResponse
from com.qxdzbc.p6.document_structure.communication.event_server.reactors.worksheet_event.DeleteMultiReactor import \
    DeleteMultiReactor
from com.qxdzbc.p6.document_structure.range.address.RangeAddresses import RangeAddresses
from com.qxdzbc.p6.document_structure.util.result.Err import Err
from com.qxdzbc.p6.document_structure.util.result.Ok import Ok
from com.qxdzbc.p6.document_structure.workbook.WorkbookImp import WorkbookImp
from com.qxdzbc.p6.document_structure.workbook.key.WorkbookKeys import WorkbookKeys
from com.qxdzbc.p6.proto.WorksheetProtos_pb2 import DeleteMultiRequestProto


class DeleteMultiReactor_test(unittest.TestCase):


    def setUp(self) -> None:
        super().setUp()

        self.wb = WorkbookImp("book1")
        self.s1 = self.wb.createNewWorksheet("Sheet1")
        self.s2 = self.wb.createNewWorksheet("Sheet2")
        self.s1.cell("A1").value = 1
        self.s1.cell("B2").value ="b2"
        self.s1.cell("B1").value ="b1"
        self.s1.cell("C3").value = "c3"
        self.s1.cell("D3").value = "d3"
        self.s1.cell("K3").value = "k3"
        self.s1.cell("X3").value = "x3"

        requestProto = DeleteMultiRequestProto()
        requestProto.worksheetName = "Sheet1"
        requestProto.workbookKey.CopyFrom(self.wb.workbookKey.toProtoObj())
        requestProto.range.extend(map(lambda r: r.toProtoObj(), [RangeAddresses.fromLabel("A1:B2")]))
        requestProto.cell.extend(
            map(lambda c: c.toProtoObj(), list(map(lambda l: CellAddresses.fromLabel(l), ["C3", "K3"]))))
        self.stdRequest = requestProto

        def getWbOk(wbKey):
            if wbKey == self.wb.workbookKey:
                return Ok(self.wb)
            else:
                return Err(AppErrors.WorkbookNotExist.report(wbKey))
        self.getWbOk =getWbOk
        self.reactor = DeleteMultiReactor(self.getWbOk)

    def test_react_standardCase(self):
        o = self.reactor.react(self.stdRequest.SerializeToString())
        self.__test_okCase(o)
        for cl in ["D3","X3"]:
            self.assertTrue(self.s1.hasCellAt(CellAddresses.fromLabel(cl)))
        for cl in ["C3","K3","A1","B1","B2"]:
            self.assertFalse(self.s1.hasCellAt(CellAddresses.fromLabel(cl)))

    def test_react_differentSheet(self):
        r = self.stdRequest
        r.worksheetName=self.s2.name
        o = self.reactor.react(r.SerializeToString())
        self.__test_okCase(o)
        for cl in ["C3", "K3", "A1", "B1", "B2","D3","X3"]:
            self.assertTrue(self.s1.hasCellAt(CellAddresses.fromLabel(cl)))

    def test_react_invalidSheet(self):
        reactor = DeleteMultiReactor(self.getWbOk)
        r = self.stdRequest
        r.worksheetName = self.s2.name + "qwewe"
        o = self.reactor.react(r.SerializeToString())
        self.__test_failCase(o)

    def test_react_invalidWb(self):
        r = self.stdRequest
        invalidWbKey = WorkbookKeys.fromNameAndPath("qwe")
        r.workbookKey.CopyFrom(invalidWbKey.toProtoObj())
        o = self.reactor.react(r.SerializeToString())
        self.__test_failCase(o)
        self.assertTrue(o.errorReport.isSameErr(AppErrors.WorkbookNotExist.report(invalidWbKey)))
        self.assertEqual(invalidWbKey,o.errorReport.data.wbKey)


    def __test_okCase(self, o:DeleteMultiResponse):
        self.assertFalse(o.isError)
        self.assertIsNone(o.errorReport)
        self.assertIsNotNone(o.newWorkbook)

    def __test_failCase(self, o:DeleteMultiResponse):
        self.assertTrue(o.isError)
        self.assertIsNotNone(o.errorReport)
        self.assertIsNone(o.newWorkbook)



if __name__ == '__main__':
    unittest.main()
