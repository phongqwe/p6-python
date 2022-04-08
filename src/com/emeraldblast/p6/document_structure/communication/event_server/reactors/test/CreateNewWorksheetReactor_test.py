import unittest

from com.emeraldblast.p6.document_structure.communication.event.data.request.CreateNewWorksheetRequest import CreateNewWorksheetRequest
from com.emeraldblast.p6.document_structure.communication.event_server.reactors.workbook.CreateNewWorksheetReactor import \
    CreateNewWorksheetReactor
from com.emeraldblast.p6.document_structure.util.result.Ok import Ok
from com.emeraldblast.p6.document_structure.workbook.WorkbookImp import WorkbookImp


class CreateNewWorksheetReactor_test(unittest.TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.wb = WorkbookImp("Book1")
        self.s1 = self.wb.createNewWorksheet("Sheet1")
        self.s2 = self.wb.createNewWorksheet("Sheet2")

        def wbGetter(identity):
            return Ok(self.wb)

        self.wbGetter = wbGetter

    def test_ok(self):
        reactor = CreateNewWorksheetReactor("zx_id", self.wbGetter)
        request = CreateNewWorksheetRequest(
            workbookKey = self.wb.workbookKey,
            newWorkSheetName = "SheetX")

        output = reactor.react(request.toProtoBytes())

        self.assertFalse(output.isError)
        self.assertIsNotNone(self.wb.getWorksheetOrNone(request.newWorksheetName))
        self.assertEqual(3, self.wb.sheetCount)

    def test_BlankName(self):
        reactor = CreateNewWorksheetReactor("zx_id", self.wbGetter)
        request = CreateNewWorksheetRequest(
            workbookKey = self.wb.workbookKey,
            newWorkSheetName = "")

        output = reactor.react(request.toProtoBytes())
        self.assertFalse(output.isError)
        self.assertNotEqual(request.newWorksheetName, output.newWorksheetName)
        self.assertEqual(3, self.wb.sheetCount)

    def test_CollidingName(self):
        reactor = CreateNewWorksheetReactor("zx_id", self.wbGetter)
        request = CreateNewWorksheetRequest(
            workbookKey = self.wb.workbookKey,
            newWorkSheetName = self.s1.name)

        output = reactor.react(request.toProtoBytes())
        self.assertTrue(output.isError)
        self.assertEqual(request.newWorksheetName, output.newWorksheetName)
        self.assertEqual(2, self.wb.sheetCount)


if __name__ == '__main__':
    unittest.main()
