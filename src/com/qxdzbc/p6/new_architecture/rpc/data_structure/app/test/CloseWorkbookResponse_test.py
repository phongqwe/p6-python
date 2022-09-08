import unittest

from com.qxdzbc.p6.new_architecture.data_structure.app_event import \
    CloseWorkbookResponse

from com.qxdzbc.p6.document_structure.util.report.error.ErrorHeader import ErrorHeader
from com.qxdzbc.p6.document_structure.util.report.error.ErrorReport import ErrorReport
from com.qxdzbc.p6.document_structure.util.result.Ok import Ok
from com.qxdzbc.p6.document_structure.workbook.key.WorkbookKeys import WorkbookKeys


class CloseWorkbookResponse_test(unittest.TestCase):
    def test_toProto_stdCase(self):
        o = CloseWorkbookResponse(
            isError = False,
            workbookKey = WorkbookKeys.fromNameAndPath("BBB"),
            windowId = "abc",
            errorReport = None
        )

        proto = o.toProtoObj()
        self.assertEqual(o.isError, proto.isError)
        self.assertEqual(o.workbookKey.toProtoObj(), proto.workbookKey)
        self.assertEqual(o.windowId, proto.windowId)
        self.assertFalse(proto.HasField("errorReport"))

    def test_toProto_stdCase_withoutWindowId(self):
        o = CloseWorkbookResponse(
            isError = False,
            workbookKey = WorkbookKeys.fromNameAndPath("BBB"),
            windowId = None,
            errorReport = None
        )

        proto = o.toProtoObj()
        self.assertEqual(o.isError, proto.isError)
        self.assertEqual(o.workbookKey.toProtoObj(), proto.workbookKey)
        self.assertFalse(proto.HasField("errorReport"))
        self.assertFalse(proto.HasField("windowId"))

    def test_toProto_error(self):
        o = CloseWorkbookResponse(
            isError = True,
            workbookKey = WorkbookKeys.fromNameAndPath("BBB"),
            windowId = "windowId",
            errorReport = ErrorReport(
                header= ErrorHeader("123","abc")
            )
        )

        proto = o.toProtoObj()
        self.assertEqual(o.isError, proto.isError)
        self.assertEqual(o.workbookKey.toProtoObj(), proto.workbookKey)
        self.assertEqual(o.windowId, proto.windowId)
        self.assertEqual(o.errorReport.toProtoObj(), proto.errorReport)

    def test_fromRs(self):
        wbk = WorkbookKeys.fromNameAndPath("abc")
        o = CloseWorkbookResponse.fromRs(Ok(wbk),None)
        self.assertFalse(o.isError)
        self.assertEqual(wbk, o.workbookKey)
        self.assertIsNone(o.windowId)
        self.assertIsNone(o.errorReport)

if __name__ == '__main__':
    unittest.main()
