import unittest

from com.qxdzbc.p6.range.address.RangeAddresses import RangeAddresses
from com.qxdzbc.p6.workbook.key.WorkbookKeys import WorkbookKeys
from com.qxdzbc.p6.range.rpc_data_structure.RangeId import RangeId
from com.qxdzbc.p6.range.rpc_data_structure.range_to_clipboard.RangeToClipboardRequest import \
    RangeToClipboardRequest
from com.qxdzbc.p6.proto.RangeProtos_pb2 import RangeOperationRequestProto


class RangeToClipboardRequest_test(unittest.TestCase):

    def setUp(self) -> None:
        super().setUp()
        self.rangeId = RangeId(
            rangeAddress = RangeAddresses.fromLabel("A1:B3"),
            wbKey = WorkbookKeys.fromNameAndPath("zz"),
            wsName = "abc"
        )

    def test_fromProto(self):
        proto = RangeOperationRequestProto(
            rangeId = self.rangeId.toProtoObj(),
            windowId="wd"
        )
        
        o = RangeToClipboardRequest.fromProto(proto)
        self.assertEqual(self.rangeId,o.rangeId)
        self.assertEqual(proto.windowId, o.windowId)

    def test_fromProto2(self):
        proto = RangeOperationRequestProto(
            rangeId = self.rangeId.toProtoObj(),
        )

        o = RangeToClipboardRequest.fromProto(proto)
        self.assertEqual(self.rangeId, o.rangeId)
        self.assertIsNone(o.windowId)


if __name__ == '__main__':
    unittest.main()
