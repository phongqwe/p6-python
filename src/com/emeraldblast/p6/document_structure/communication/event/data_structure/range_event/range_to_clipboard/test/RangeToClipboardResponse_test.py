import unittest

from com.emeraldblast.p6.document_structure.communication.event.data_structure.common.ErrorIndicator import \
    ErrorIndicator
from com.emeraldblast.p6.document_structure.communication.event.data_structure.range_event.RangeId import RangeId
from com.emeraldblast.p6.document_structure.communication.event.data_structure.range_event.range_to_clipboard.RangeToClipboardResponse import \
    RangeToClipboardResponse
from com.emeraldblast.p6.document_structure.range.address.RangeAddresses import RangeAddresses
from com.emeraldblast.p6.document_structure.workbook.key.WorkbookKeys import WorkbookKeys


class RangeToClipboardResponse_test(unittest.TestCase):
    def test_toProto(self):
        o = RangeToClipboardResponse(
            errorIndicator = ErrorIndicator.noError(),
            rangeId = RangeId(
                rangeAddress = RangeAddresses.fromLabel("@A1:B3"),
                workbookKey = WorkbookKeys.fromNameAndPath(""),
                worksheetName = "abc"
            ),
            windowId = "asd"
        )

        proto = o.toProtoObj()
        self.assertEqual(o.errorIndicator.toProtoObj(), proto.errorIndicator)
        self.assertEqual(o.rangeId.toProtoObj(), proto.rangeId)
        self.assertEqual(o.windowId, proto.windowId)

    def test_toProto2(self):
        o = RangeToClipboardResponse(
            errorIndicator = ErrorIndicator.noError(),
            rangeId = RangeId(
                rangeAddress = RangeAddresses.fromLabel("@A1:B3"),
                workbookKey = WorkbookKeys.fromNameAndPath(""),
                worksheetName = "abc"
            ),
            windowId = None
        )
        proto = o.toProtoObj()
        self.assertEqual(o.errorIndicator.toProtoObj(), proto.errorIndicator)
        self.assertEqual(o.rangeId.toProtoObj(), proto.rangeId)
        self.assertFalse(proto.HasField("windowId"))


if __name__ == '__main__':
    unittest.main()
