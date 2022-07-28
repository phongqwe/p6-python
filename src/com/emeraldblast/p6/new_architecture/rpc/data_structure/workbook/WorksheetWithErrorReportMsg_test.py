import unittest

from com.emeraldblast.p6.document_structure.util.for_test import TestUtils

from com.emeraldblast.p6.document_structure.worksheet.WorksheetImp import WorksheetImp
from com.emeraldblast.p6.new_architecture.rpc.data_structure.workbook.WorksheetWithErrorReportMsg import \
    WorksheetWithErrorReportMsg


class WorksheetWithErrorReportMsg_test(unittest.TestCase):
    def test_from_toProto(self):
        o1=WorksheetWithErrorReportMsg(
            worksheet = WorksheetImp("ws1",None),
            errorReport = None
        )
        p1 = o1.toProtoObj()
        self.assertFalse(p1.HasField("errorReport"))
        self.assertEqual(o1.worksheet.toProtoObj(),p1.worksheet)

        o1 = WorksheetWithErrorReportMsg(
            worksheet = None,
            errorReport = TestUtils.TestErrorReport
        )
        p1 = o1.toProtoObj()
        self.assertFalse(p1.HasField("worksheet"))
        self.assertEqual(TestUtils.TestErrorReport.toProtoObj(), p1.errorReport)

if __name__ == '__main__':
    unittest.main()
