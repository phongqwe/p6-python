import unittest
from unittest.mock import MagicMock

from com.emeraldblast.p6.document_structure.communication.event_server.reactors.EventServerReactors import \
    EventServerReactors
from com.emeraldblast.p6.document_structure.communication.event_server.reactors.worksheet_event.RenameWorksheetReactor import \
    RenameWorksheetReactor
from com.emeraldblast.p6.document_structure.communication.reactor.EventReactor import EventReactor
from com.emeraldblast.p6.document_structure.util.result.Ok import Ok
from com.emeraldblast.p6.document_structure.workbook.WorkbookErrors import WorkbookErrors
from com.emeraldblast.p6.document_structure.workbook.WorkbookImp import WorkbookImp
from com.emeraldblast.p6.document_structure.workbook.key.WorkbookKeys import WorkbookKeys
from com.emeraldblast.p6.document_structure.worksheet.WorksheetErrors import WorksheetErrors
from com.emeraldblast.p6.proto.WorksheetProtos_pb2 import RenameWorksheetRequestProto

from com.emeraldblast.p6.document_structure.communication.event.data_structure.worksheet_event.RenameWorksheetResponse import \
    RenameWorksheetResponse


class RenameWorksheetReactor_test(unittest.TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.wb = WorkbookImp("Book1")
        self.s1 = self.wb.createNewWorksheet("Sheet1")
        self.s2 = self.wb.createNewWorksheet("Sheet2")
        def wbGetter(wbKey):
            return Ok(self.wb)
        self.wbGetter = wbGetter
        def appGetter():
            return MagicMock()

        self.appGetter = appGetter
        self.er = EventServerReactors(wbGetter,appGetter = appGetter)
        self.reactor = RenameWorksheetReactor("x", self.wbGetter)

    def test_renameReactor_Ok(self):
        inputData = RenameWorksheetRequestProto()
        inputData.workbookKey.CopyFrom(WorkbookKeys.fromNameAndPath("Book1", None).toProtoObj())
        inputData.oldName = self.s1.name
        inputData.newName = "NewName"
        out = self.reactor.react(inputData.SerializeToString())
        self.assertFalse(out.isError)
        print(out)
        print(out.toProtoBytes())
        self.assertEqual(inputData.oldName, out.oldName)
        self.assertEqual(self.s1.name, out.newName)
        self.assertEqual(out.workbookKey, self.wb.workbookKey)

    def test_renameReactor_Fail_EmpyNewName(self):

        inputData = RenameWorksheetRequestProto()
        inputData.workbookKey.CopyFrom(WorkbookKeys.fromNameAndPath("Book1", None).toProtoObj())
        inputData.oldName = self.s1.name
        inputData.newName = ""

        out = self.reactor.react(inputData.SerializeToString())
        print(out)
        print(out.toProtoBytes)
        self.assertTrue(out.isError)
        self.assertTrue(self.s1.name, out.oldName)
        self.assertEqual(out.workbookKey, self.wb.workbookKey)
        errReport = out.errorReport
        self.assertEqual(WorksheetErrors.IllegalNameReport.header, errReport.header)

    def test_renameReactor_Fail_CollidingName(self):
        inputData = RenameWorksheetRequestProto()
        inputData.workbookKey.CopyFrom(self.wb.workbookKey.toProtoObj())
        inputData.oldName = self.s1.name
        inputData.newName = self.s2.name

        out = self.reactor.react(inputData.SerializeToString())
        print(out)
        self.assertTrue(out.isError)
        self.assertTrue(self.s1.name, out.oldName)
        self.assertEqual(out.workbookKey, self.wb.workbookKey)
        errReport = out.errorReport
        self.assertEqual(WorkbookErrors.WorksheetAlreadyExistReport.header, errReport.header)


if __name__ == '__main__':
    unittest.main()
