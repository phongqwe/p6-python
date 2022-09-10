import unittest
from pathlib import Path

from com.qxdzbc.p6.document_structure.util.report.error.ErrorReport import ErrorReport
from com.qxdzbc.p6.document_structure.workbook.WorkbookErrors import WorkbookErrors
from com.qxdzbc.p6.document_structure.workbook.key.WorkbookKeys import WorkbookKeys
from com.qxdzbc.p6.new_architecture.rpc.data_structure.workbook.save_wb.SaveWorkbookResponse import \
    SaveWorkbookResponse


class SaveWorkbookResponse_test(unittest.TestCase):
    def test_toProto(self):
        WorkbookErrors.WorksheetNotExistReport(123)
        o = SaveWorkbookResponse(
            errorReport = None,
            wbKey = WorkbookKeys.fromNameAndPath("B1", Path("qwe")),
            path = "123/234"
        )
        p = o.toProtoObj()
        self.assertFalse(p.HasField("errorReport"))
        self.assertEqual(o.wbKey, WorkbookKeys.fromProto(p.wbKey))
        self.assertEqual(o.path, p.path)

    def test_toProto_errorCase(self):

        o = SaveWorkbookResponse(
            errorReport = WorkbookErrors.WorksheetNotExistReport(123),
            wbKey = WorkbookKeys.fromNameAndPath("B1", Path("qwe")),
            path = "123/234"
        )
        p = o.toProtoObj()
        self.assertTrue(p.HasField("errorReport"))
        self.assertEqual(o.wbKey, WorkbookKeys.fromProto(p.wbKey))
        self.assertEqual(o.errorReport.header, ErrorReport.fromProto(p.errorReport).header)
        self.assertEqual(o.path, p.path)

if __name__ == '__main__':
    unittest.main()
