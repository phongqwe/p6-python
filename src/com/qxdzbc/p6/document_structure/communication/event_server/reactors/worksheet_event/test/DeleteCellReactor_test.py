import unittest

from com.qxdzbc.p6.document_structure.app.errors.AppErrors import AppErrors
from com.qxdzbc.p6.document_structure.cell.address.CellIndex import CellIndex
from com.qxdzbc.p6.document_structure.communication.event.data_structure.worksheet_event.DeleteCellRequest import \
    DeleteCellRequest
from com.qxdzbc.p6.document_structure.communication.event_server.reactors.worksheet_event.DeleteCellReactor import \
    DeleteCellReactor
from com.qxdzbc.p6.document_structure.range.RangeErrors import RangeErrors
from com.qxdzbc.p6.document_structure.util.result.Err import Err
from com.qxdzbc.p6.document_structure.util.result.Ok import Ok
from com.qxdzbc.p6.document_structure.workbook.WorkbookErrors import WorkbookErrors
from com.qxdzbc.p6.document_structure.workbook.WorkbookImp import WorkbookImp


class DeleteCellReactor_test(unittest.TestCase):

    def setUp(self) -> None:
        super().setUp()
        self.wb = WorkbookImp("Book1")
        self.s1 = self.wb.createNewWorksheet("Sheet1")
        self.s2 = self.wb.createNewWorksheet("Sheet2")
        self.s1.cell((1, 1)).value = 11
        self.s1.cell((2, 2)).value = 22
        self.s1.cell((3, 3)).value = 33

        self.s2.cell((1, 1)).value = 211
        self.s2.cell((2, 2)).value = 222
        self.s2.cell((3, 3)).value = 233

        def wbGetter(identity):
            return Ok(self.wb)

        self.wbGetter = wbGetter
        self.reactor = DeleteCellReactor("uid", self.wbGetter)

    def checkIdentity(self, i, o):
        self.assertEqual(i.workbookKey, o.workbookKey)
        self.assertEqual(i.worksheetName, o.worksheetName)
        self.assertEqual(i.cellAddress, o.cellAddress)

    def checkErr(self, i, o):
        self.checkIdentity(i, o)
        self.assertTrue(o.isError)
        self.assertIsNotNone(o.errorReport)

    def test_reactor_failToToDeleteCell(self):
        i = DeleteCellRequest(
            workbookKey = self.wb.workbookKey,
            worksheetName = self.s1.name,
            cellAddress = CellIndex(-1, 1)
        )
        o = self.reactor.react(i.toProtoBytes())
        self.checkErr(i, o)
        print(o.toProtoObj())
        self.assertEqual(RangeErrors.CellNotInRangeReport.header,o.errorReport.header)

    def test_reactor_failToGetWorksheet(self):
        i = DeleteCellRequest(
            workbookKey = self.wb.workbookKey,
            worksheetName = "InvSheet",
            cellAddress = CellIndex(1, 1)
        )
        o = self.reactor.react(i.toProtoBytes())
        self.checkErr(i, o)
        self.assertEqual(WorkbookErrors.WorksheetNotExistReport.header,o.errorReport.header)

    def test_react_failToGetWb(self):
        err = Err(AppErrors.WorkbookNotExist.report("invalidWB"))

        def wbGetterFail(identity):
            return err

        reactor = DeleteCellReactor("uid", wbGetterFail)
        i = DeleteCellRequest(
            workbookKey = self.wb.workbookKey,
            worksheetName = self.s1.name,
            cellAddress = CellIndex(1, 1)
        )
        o = reactor.react(i.toProtoBytes())
        self.checkErr(i, o)
        self.assertEqual(11, self.s1.cell((1, 1)).bareValue)
        self.assertIsNotNone(err.err.header, o.errorReport.header)

    def test_react_ok(self):
        i = DeleteCellRequest(
            workbookKey = self.wb.workbookKey,
            worksheetName = self.s1.name,
            cellAddress = CellIndex(1, 1)
        )
        o = self.reactor.react(i.toProtoBytes())
        self.checkIdentity(i, o)
        self.assertEqual(None, self.s1.cell((1, 1)).bareValue)
        for cell in self.s1.cells:
            self.assertNotEqual(CellIndex(1, 1), cell.address)
            self.assertIsNotNone(cell.value, cell.address)

        self.assertEqual(False, o.isError)
        self.assertIsNone(o.errorReport)


if __name__ == '__main__':
    unittest.main()
