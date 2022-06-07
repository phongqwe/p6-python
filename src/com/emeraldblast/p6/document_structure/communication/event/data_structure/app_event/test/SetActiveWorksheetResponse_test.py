import unittest
from pathlib import Path

from com.emeraldblast.p6.document_structure.communication.event.P6EventTableImp import P6EventTableImp
from com.emeraldblast.p6.document_structure.communication.event.data_structure.app_event.SetActiveWorksheetResponse import \
    SetActiveWorksheetResponse
from com.emeraldblast.p6.document_structure.util.report.error.ErrorHeader import ErrorHeader
from com.emeraldblast.p6.document_structure.util.report.error.ErrorReport import ErrorReport
from com.emeraldblast.p6.document_structure.workbook.key.WorkbookKeys import WorkbookKeys
from com.emeraldblast.p6.proto.AppEventProtos_pb2 import SetActiveWorksheetResponseProto


class SetActiveWorksheetResponse_test(unittest.TestCase):

    def test_toEventData(self):
        k = WorkbookKeys.fromNameAndPath("B1", Path("abc").absolute())
        er = ErrorReport(
            header = ErrorHeader("h1", "d1"),
            data = 12345
        )
        res = SetActiveWorksheetResponse(
            workbookKey = k,
            worksheetName = "name345",
            isError = False,
            errorReport = er
        )
        edt=res.toEventData()
        self.assertEqual(P6EventTableImp.i().getEventForClazz(SetActiveWorksheetResponse),edt.event)
        self.assertEqual(res,edt.data)


    def test_fromProto(self):
        k = WorkbookKeys.fromNameAndPath("B1",Path("abc").absolute())
        er = ErrorReport(
            header= ErrorHeader("h1","d1"),
            data = 12345
        )
        proto = SetActiveWorksheetResponseProto()
        proto.workbookKey.CopyFrom(k.toProtoObj())
        proto.worksheetName = "Name123"
        proto.isError=True
        proto.errorReport.CopyFrom(er.toProtoObj())

        o = SetActiveWorksheetResponse.fromProtoBytes(proto.SerializeToString())
        self.assertEqual(k,o.workbookKey)
        self.assertEqual(proto.worksheetName, o.worksheetName)
        self.assertEqual(True, proto.isError)
        self.assertEqual(er.header, o.errorReport.header)
    def test_toProto(self):
        k = WorkbookKeys.fromNameAndPath("B1", Path("abc").absolute())
        er = ErrorReport(
            header = ErrorHeader("h1", "d1"),
            data = 12345
        )
        res = SetActiveWorksheetResponse(
            workbookKey = k,
            worksheetName = "name345",
            isError = False,
            errorReport = er
        )

        proto = res.toProtoObj()
        self.assertEqual(k.toProtoObj(), proto.workbookKey)
        self.assertEqual(res.worksheetName, proto.worksheetName)
        self.assertEqual(False, proto.isError)
        self.assertEqual(er.toProtoObj(), proto.errorReport)

if __name__ == '__main__':
    unittest.main()
