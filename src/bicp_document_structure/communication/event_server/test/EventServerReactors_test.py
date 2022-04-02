import unittest

from bicp_document_structure.communication.event.data.response.RenameWorksheetData import RenameWorksheetResponseData
from bicp_document_structure.communication.event_server.msg.P6Message import P6Message

from bicp_document_structure.communication.event_server.EventServerReactors import EventServerReactors
from bicp_document_structure.communication.internal_reactor.BaseReactor import BasicReactor
from bicp_document_structure.communication.internal_reactor.EventReactor import EventReactor
from bicp_document_structure.communication.proto.WorksheetProtos_pb2 import RenameWorksheetResponseProto, RenameWorksheetRequestProto
from bicp_document_structure.util.result.Ok import Ok
from bicp_document_structure.workbook.WorkbookErrors import WorkbookErrors
from bicp_document_structure.workbook.WorkbookImp import WorkbookImp
from bicp_document_structure.workbook.key.WorkbookKeys import WorkbookKeys
from bicp_document_structure.worksheet.WorksheetErrors import WorksheetErrors


class EventServerReactors_test(unittest.TestCase):

    def setUp(self) -> None:
        super().setUp()
        self.wb = WorkbookImp("Book1")
        self.s1 = self.wb.createNewWorksheet("Sheet1")
        self.s2 = self.wb.createNewWorksheet("Sheet2")
        def wbGetter(identity):
            return Ok(self.wb)
        self.er = EventServerReactors(wbGetter)

    def test_renameReactor_Ok(self):
        reactor: EventReactor[bytes, RenameWorksheetResponseData] = self.er.renameWorksheet()
        inputData = RenameWorksheetRequestProto()
        inputData.workbookKey.CopyFrom(WorkbookKeys.fromNameAndPath("Book1", None).toProtoObj())
        inputData.oldName = self.s1.name
        inputData.newName = "NewName"

        out = reactor.react(inputData.SerializeToString())
        print(out)
        print(out.toProtoBytes())
        self.assertEqual(inputData.oldName, out.oldName)
        self.assertEqual(self.s1.name, out.newName)
        self.assertEqual(out.workbookKey, self.wb.workbookKey)

    def test_renameReactor_Fail_EmpyNewName(self):
        reactor: EventReactor[bytes, RenameWorksheetResponseData] = self.er.renameWorksheet()
        inputData = RenameWorksheetRequestProto()
        inputData.workbookKey.CopyFrom(WorkbookKeys.fromNameAndPath("Book1", None).toProtoObj())
        inputData.oldName = self.s1.name
        inputData.newName = ""

        out = reactor.react(inputData.SerializeToString())
        print(out)
        print(out.toProtoBytes)
        self.assertTrue(out.isError)
        self.assertTrue(self.s1.name, out.oldName)
        self.assertEqual(out.workbookKey, self.wb.workbookKey)
        errReport = out.errorReport
        self.assertEqual(WorksheetErrors.IllegalNameReport.header, errReport.header)

    def test_renameReactor_Fail_CollidingName(self):
        reactor: EventReactor[bytes, RenameWorksheetResponseData] = self.er.renameWorksheet()
        inputData = RenameWorksheetRequestProto()
        inputData.workbookKey.CopyFrom(self.wb.workbookKey.toProtoObj())
        inputData.oldName = self.s1.name
        inputData.newName = self.s2.name

        out = reactor.react(inputData.SerializeToString())
        print(out)
        self.assertTrue(out.isError)
        self.assertTrue(self.s1.name, out.oldName)
        self.assertEqual(out.workbookKey, self.wb.workbookKey)
        errReport = out.errorReport
        self.assertEqual(WorkbookErrors.WorksheetAlreadyExistReport.header, errReport.header)


if __name__ == '__main__':
    unittest.main()
