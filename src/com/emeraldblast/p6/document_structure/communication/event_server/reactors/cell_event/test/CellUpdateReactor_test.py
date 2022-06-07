import unittest

from com.emeraldblast.p6.document_structure.app.errors.AppErrors import AppErrors
from com.emeraldblast.p6.document_structure.cell.address.CellAddresses import CellAddresses
from com.emeraldblast.p6.document_structure.communication.event.P6Events import P6Events
from com.emeraldblast.p6.document_structure.communication.event_server.reactors.cell_event.CellUpdateReactor import \
    CellUpdateReactor
from com.emeraldblast.p6.document_structure.util.result.Err import Err
from com.emeraldblast.p6.document_structure.util.result.Ok import Ok
from com.emeraldblast.p6.document_structure.workbook.WorkbookErrors import WorkbookErrors
from com.emeraldblast.p6.document_structure.workbook.WorkbookImp import WorkbookImp


class CellUpdateReactor_test(unittest.TestCase):

    def setUp(self) -> None:
        super().setUp()
        self.wb = WorkbookImp("Book1")
        self.s1 = self.wb.createNewWorksheet("Sheet1")
        self.s2 = self.wb.createNewWorksheet("Sheet2")

        def wbGetter(identity):
            return Ok(self.wb)

        def wbGetterFail(identity):
            return Err(
                AppErrors.WorkbookNotExist("invalidWB")
            )

        self.wbGetter = wbGetter


    def test_OkBlankContent(self):
        reactor = CellUpdateReactor("id", self.wbGetter)

        self.wb.getWorksheet("Sheet1").cell((1,1)).value=123

        request = P6Events.Cell.Update.Request(
            workbookKey = self.wb.workbookKey,
            worksheetName = "Sheet1",
            cellAddress = CellAddresses.fromRowCol(1, 1),
            value = "", formula = ""
        )
        outObj = reactor.react(request.toProtoBytes())
        self.assertFalse(outObj.isError)
        self.assertIsNone(outObj.errorReport)
        self.assertIsNotNone(outObj.newWorkbook)
        outProto = (outObj.newWorkbook.toProtoObj())
        print(outProto)
        self.assertEqual(None, outObj.newWorkbook.getWorksheetOrNone("Sheet1").cell((1, 1)).value)
        self.assertEqual("", outObj.newWorkbook.getWorksheetOrNone("Sheet1").cell((1, 1)).displayValue)

    def test_invalidWB(self):
        err = AppErrors.WorkbookNotExist("invalidWB")

        def wbGetterFail(identity):
            return Err(err)

        reactor = CellUpdateReactor("id", wbGetterFail)
        request = P6Events.Cell.Update.Request(
            workbookKey = self.wb.workbookKey,
            worksheetName = "Sheet1",
            cellAddress = CellAddresses.fromRowCol(1, 1),
            value = "123", formula = ""
        )
        outObj = reactor.react(request.toProtoBytes())
        self.assertTrue(outObj.isError)
        self.assertIsNone(outObj.newWorkbook)
        self.assertIsNotNone(outObj.errorReport)
        self.assertEqual(err, outObj.errorReport)

    def test_invalidSheet(self):
        reactor = CellUpdateReactor("id", self.wbGetter)
        request = P6Events.Cell.Update.Request(
            workbookKey = self.wb.workbookKey,
            worksheetName = "Sheet1000",
            cellAddress = CellAddresses.fromRowCol(1, 1),
            value = "123", formula = ""
        )
        outObj = reactor.react(request.toProtoBytes())
        self.assertTrue(outObj.isError)
        self.assertIsNone(outObj.newWorkbook)
        self.assertIsNotNone(outObj.errorReport)
        self.assertEqual(WorkbookErrors.WorksheetNotExistReport.header, outObj.errorReport.header)

    def test_Ok(self):
        reactor = CellUpdateReactor("id", self.wbGetter)
        request = P6Events.Cell.Update.Request(
            workbookKey = self.wb.workbookKey,
            worksheetName = "Sheet1",
            cellAddress = CellAddresses.fromRowCol(1, 1),
            value = "123", formula = ""
        )
        outObj = reactor.react(request.toProtoBytes())
        self.assertFalse(outObj.isError)
        self.assertIsNone(outObj.errorReport)
        self.assertIsNotNone(outObj.newWorkbook)
        self.assertEqual(request.value, outObj.newWorkbook.getWorksheetOrNone("Sheet1").cell((1, 1)).value)

    def test_OkFormula(self):
        reactor = CellUpdateReactor("id", self.wbGetter)
        request = P6Events.Cell.Update.Request(
            workbookKey = self.wb.workbookKey,
            worksheetName = "Sheet1",
            cellAddress = CellAddresses.fromRowCol(1, 1),
            value = None, formula = "=SCRIPT(1+2)"
        )
        outObj = reactor.react(request.toProtoBytes())
        self.assertFalse(outObj.isError)
        self.assertIsNone(outObj.errorReport)
        self.assertIsNotNone(outObj.newWorkbook)
        outProto = (outObj.newWorkbook.toProtoObj())
        print(outProto)
        self.assertEqual(3, outObj.newWorkbook.getWorksheetOrNone("Sheet1").cell((1, 1)).value)
        self.assertEqual("3", outProto.worksheet[0].cell[0].value)


if __name__ == '__main__':
    unittest.main()
