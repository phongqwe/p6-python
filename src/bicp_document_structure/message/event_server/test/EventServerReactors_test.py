import unittest

from bicp_document_structure.app.GlobalScope import setIPythonGlobals
from bicp_document_structure.app.UserFunctions import startApp, restartApp, getApp, getActiveWorkbook, getWorkbook
from bicp_document_structure.message.P6Message import P6Message
from bicp_document_structure.message.event.P6Events import P6Events
from bicp_document_structure.message.event.reactor.BaseReactor import BasicReactor
from bicp_document_structure.message.event_server.EventServerReactors import EventServerReactors
from bicp_document_structure.message.proto.WorkbookProtoMsg_pb2 import RenameWorksheetProto, RenameRequestProto
from bicp_document_structure.workbook.WorkbookErrors import WorkbookErrors
from bicp_document_structure.workbook.key.WorkbookKeys import WorkbookKeys
from bicp_document_structure.worksheet.WorksheetErrors import WorksheetErrors


class EventServerReactors_test(unittest.TestCase):

    def setUp(self) -> None:
        super().setUp()
        setIPythonGlobals(globals())
        startApp()
        restartApp()
        getApp().createNewWorkbook("Book1")
        getActiveWorkbook().createNewWorksheet("Sheet1")
        getActiveWorkbook().createNewWorksheet("Sheet2")
        self.wb = getWorkbook("Book1")
        self.s1 = self.wb.getWorksheet("Sheet1")
        self.s2 = self.wb.getWorksheet("Sheet2")
        def wbGetter(identity):
            return getApp().getBareWorkbookRs(identity)
        self.er = EventServerReactors(wbGetter)

    def test_renameReactor_Ok(self):
        reactor: BasicReactor[P6Message, RenameWorksheetProto] = self.er.renameWorksheet()
        inputData = RenameRequestProto()
        inputData.workbookKey.CopyFrom(WorkbookKeys.fromNameAndPath("Book1", None).toProtoObj())
        inputData.oldName = self.s1.name
        inputData.newName = "NewName"
        input = P6Message.create(
            event = P6Events.Worksheet.Rename.event,
            data = inputData.SerializeToString()
        )
        out = reactor.react(input)
        print(out)
        self.assertEqual(inputData.oldName, out.oldName)
        self.assertEqual(self.s1.name, out.newName)
        self.assertEqual(out.workbookKey, self.wb.workbookKey.toProtoObj())

    def test_renameReactor_Fail_EmpyNewName(self):
        reactor: BasicReactor[P6Message, RenameWorksheetProto] = self.er.renameWorksheet()
        inputData = RenameRequestProto()
        inputData.workbookKey.CopyFrom(WorkbookKeys.fromNameAndPath("Book1", None).toProtoObj())
        inputData.oldName = self.s1.name
        inputData.newName = ""
        input = P6Message.create(
            event = P6Events.Worksheet.Rename.event,
            data = inputData.SerializeToString()
        )
        out = reactor.react(input)
        print(out)
        self.assertTrue(out.isError)
        self.assertTrue(self.s1.name, out.oldName)
        self.assertEqual(out.workbookKey, self.wb.workbookKey.toProtoObj())
        errReport = out.errorReport
        self.assertEqual(WorksheetErrors.IllegalName.header.errorCode, errReport.errorCode)

    def test_renameReactor_Fail_CollidingName(self):
        reactor: BasicReactor[P6Message, RenameWorksheetProto] = self.er.renameWorksheet()
        inputData = RenameRequestProto()
        inputData.workbookKey.CopyFrom(self.wb.workbookKey.toProtoObj())
        inputData.oldName = self.s1.name
        inputData.newName = self.s2.name
        input = P6Message.create(
            event = P6Events.Worksheet.Rename.event,
            data = inputData.SerializeToString()
        )
        out = reactor.react(input)
        print(out)
        self.assertTrue(out.isError)
        self.assertTrue(self.s1.name, out.oldName)
        self.assertEqual(out.workbookKey, self.wb.workbookKey.toProtoObj())
        errReport = out.errorReport
        self.assertEqual(WorkbookErrors.WorksheetAlreadyExistReport.header.errorCode, errReport.errorCode)


if __name__ == '__main__':
    unittest.main()
