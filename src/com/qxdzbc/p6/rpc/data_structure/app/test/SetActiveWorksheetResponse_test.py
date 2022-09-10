import unittest
from pathlib import Path


from com.qxdzbc.p6.util.report.error.ErrorHeader import ErrorHeader
from com.qxdzbc.p6.util.report.error.ErrorReport import ErrorReport
from com.qxdzbc.p6.workbook.key.WorkbookKeys import WorkbookKeys
from com.qxdzbc.p6.rpc.data_structure.app.SetActiveWorksheetResponse import SetActiveWorksheetResponse
from com.qxdzbc.p6.proto.AppProtos_pb2 import SetActiveWorksheetResponseProto


class SetActiveWorksheetResponse_test(unittest.TestCase):


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
