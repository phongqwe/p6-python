import unittest

from com.emeraldblast.p6.document_structure.communication.event.data_structure.app_event.CloseWorkbookRequest import \
    CloseWorkbookRequest
from com.emeraldblast.p6.document_structure.workbook.key.WorkbookKeys import WorkbookKeys
from com.emeraldblast.p6.proto.AppEventProtos_pb2 import CloseWorkbookRequestProto


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
