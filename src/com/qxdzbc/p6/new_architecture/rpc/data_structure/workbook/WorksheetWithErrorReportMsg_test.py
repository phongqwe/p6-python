import unittest

from com.qxdzbc.p6.document_structure.util.for_test import TestUtils
from com.qxdzbc.p6.new_architecture.rpc.data_structure.workbook.WorksheetWithErrorReportMsg import \
    WorksheetWithErrorReportMsg


class WorksheetWithErrorReportMsg_test(unittest.TestCase):
    def test_from_toProto(self):
        o1=WorksheetWithErrorReportMsg(
            wsName = "ws1",
            errorReport = None
        )
        p1 = o1.toProtoObj()
        self.assertFalse(p1.HasField("errorReport"))
        self.assertEqual(o1.wsName, p1.wsName)

        o1 = WorksheetWithErrorReportMsg(
            wsName = None,
            errorReport = TestUtils.TestErrorReport
        )
        p1 = o1.toProtoObj()
        self.assertFalse(p1.HasField("wsName"))
        self.assertEqual(TestUtils.TestErrorReport.toProtoObj(), p1.errorReport)

if __name__ == '__main__':
    unittest.main()
