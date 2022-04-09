import unittest

from com.emeraldblast.p6.document_structure.app.AppImp import AppImp
from com.emeraldblast.p6.document_structure.app.errors.AppErrors import AppErrors
from com.emeraldblast.p6.document_structure.app.workbook_container.WorkbookContainerImp import WorkbookContainerImp
from com.emeraldblast.p6.document_structure.communication.event.data_structure.app_event.SetActiveWorksheetRequest import \
    SetActiveWorksheetRequest
from com.emeraldblast.p6.document_structure.communication.event_server.reactors.app.SetActiveWorksheetReactor import \
    SetActiveWorksheetReactor
from com.emeraldblast.p6.document_structure.workbook.WorkbookErrors import WorkbookErrors
from com.emeraldblast.p6.document_structure.workbook.WorkbookImp import WorkbookImp
from com.emeraldblast.p6.document_structure.workbook.key.WorkbookKeys import WorkbookKeys


class SetActiveWorksheetReactor_test(unittest.TestCase):

    def setUp(self) -> None:
        self.wb1 = WorkbookImp("wb1")
        self.s11 = self.wb1.createNewWorksheet("S11")
        self.s12 = self.wb1.createNewWorksheet("S12")
        self.wb2 = WorkbookImp("wb2")
        self.s21 = self.wb2.createNewWorksheet("S21")
        self.s22 = self.wb2.createNewWorksheet("S22")

        self.wbCont = WorkbookContainerImp({
            self.wb1.workbookKey: self.wb1,
            self.wb2.workbookKey: self.wb2
        })

        self.app = AppImp(workbookContainer = self.wbCont)
        self.app.setActiveWorkbook(self.wb1.workbookKey)
        self.wb1.setActiveWorksheet(self.s11.name)

        def appGetter():
            return self.app

        self.appGetter = appGetter
        self.reactor = SetActiveWorksheetReactor("id", self.appGetter)

    def test_create(self):
        self.assertEqual(self.appGetter, self.reactor.appGetter)

    def test_react_Ok(self):
        o = self.reactor.react(
            SetActiveWorksheetRequest(
                workbookKey = self.wb2.workbookKey,
                worksheetName = self.s22.name
            ).toProtoBytes()
        )
        self.assertFalse(o.isError)
        self.assertEqual(o.workbookKey, self.wb2.workbookKey)
        self.assertEqual(o.worksheetName, self.s22.name)
        self.assertIsNone(o.errorReport)

        self.assertEqual(self.s22, self.wb2.activeWorksheet)

        # ensure that active workbook is not changed
        self.assertEqual(self.wb1, self.app.activeWorkbook)

    def test_react_invalidWorkbook(self):
        iwb = WorkbookKeys.fromNameAndPath("INVALID", None)
        o = self.reactor.react(
            SetActiveWorksheetRequest(
                workbookKey = iwb,
                worksheetName = self.s22.name
            ).toProtoBytes()
        )

        self.assertTrue(o.isError)
        self.assertIsNotNone(o.errorReport)
        self.assertEqual(AppErrors.WorkbookNotExist.header,o.errorReport.header)
        self.assertEqual(iwb, o.workbookKey)
        self.assertEqual(self.s22.name, o.worksheetName)

    def test_react_invalidWorksheet(self):
        iwb = self.wb2.workbookKey
        iname = "InvalidName"
        o = self.reactor.react(
            SetActiveWorksheetRequest(
                workbookKey = iwb,
                worksheetName = iname
            ).toProtoBytes()
        )

        self.assertTrue(o.isError)
        self.assertIsNotNone(o.errorReport)
        self.assertEqual(WorkbookErrors.WorksheetNotExistReport.header,o.errorReport.header)
        self.assertEqual(iwb, o.workbookKey)
        self.assertEqual(iname, o.worksheetName)

    def test_react_blankWorksheetName(self):
        iwb = self.wb2.workbookKey
        iname = ""
        o = self.reactor.react(
            SetActiveWorksheetRequest(
                workbookKey = iwb,
                worksheetName = iname
            ).toProtoBytes()
        )

        self.assertTrue(o.isError)
        self.assertIsNotNone(o.errorReport)
        self.assertEqual(WorkbookErrors.WorksheetNotExistReport.header,o.errorReport.header)
        self.assertEqual(iwb, o.workbookKey)
        self.assertEqual(iname, o.worksheetName)


if __name__ == '__main__':
    unittest.main()
