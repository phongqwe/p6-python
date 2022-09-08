import unittest

from com.qxdzbc.p6.new_architecture.data_structure.app_event import \
    CloseWorkbookRequest

from com.qxdzbc.p6.document_structure.workbook.key.WorkbookKeys import WorkbookKeys
from com.qxdzbc.p6.proto.AppEventProtos_pb2 import CloseWorkbookRequestProto


class CloseWorkbookRequest_test(unittest.TestCase):
    def test_fromProtoBytes_no_windowId(self):
        wbKey = WorkbookKeys.fromNameAndPath("BOokx")
        proto = CloseWorkbookRequestProto(
            workbookKey = wbKey.toProtoObj()
        )
        o = CloseWorkbookRequest.fromProtoBytes(proto.SerializeToString())
        self.assertEqual(wbKey, o.workbookKey)
        self.assertIsNone(o.windowId)

    def test_fromProtoBytes_valid_windowId(self):
        wbKey = WorkbookKeys.fromNameAndPath("BOokx")
        proto = CloseWorkbookRequestProto(
            workbookKey = wbKey.toProtoObj(),
            windowId = "windowId"
        )
        o = CloseWorkbookRequest.fromProtoBytes(proto.SerializeToString())
        self.assertEqual(wbKey, o.workbookKey)
        self.assertEqual(proto.windowId, o.windowId)


if __name__ == '__main__':
    unittest.main()
