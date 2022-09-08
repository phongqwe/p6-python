import unittest

from com.qxdzbc.p6.new_architecture.data_structure import \
    RangeToClipboardResponse

from com.qxdzbc.p6.document_structure.range.address.RangeAddresses import RangeAddresses
from com.qxdzbc.p6.document_structure.workbook.key.WorkbookKeys import WorkbookKeys
from com.qxdzbc.p6.new_architecture.communication import P6EventTableImp
from com.qxdzbc.p6.new_architecture.rpc.data_structure.common.ErrorIndicator import \
    ErrorIndicator
from com.qxdzbc.p6.new_architecture.rpc.data_structure.range.RangeId import RangeId
from com.qxdzbc.p6.proto.RangeProtos_pb2 import RangeToClipboardResponseProto


class RangeToClipboardResponse_test(unittest.TestCase):

    def test_toEventData(self):
        o = RangeToClipboardResponse(
            errorIndicator = ErrorIndicator.noError(),
            rangeId = RangeId(
                rangeAddress = RangeAddresses.fromLabel("A1:B3"),
                workbookKey = WorkbookKeys.fromNameAndPath(""),
                worksheetName = "abc"
            ),
            windowId = "asd"
        )

        edt = o.toEventData()
        self.assertEqual(P6EventTableImp.i().getEventForClazz(RangeToClipboardResponse),edt.event)
        self.assertEqual(o, edt.data)

    def test_toProto(self):
        o = RangeToClipboardResponse(
            errorIndicator = ErrorIndicator.noError(),
            rangeId = RangeId(
                rangeAddress = RangeAddresses.fromLabel("A1:B3"),
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
                rangeAddress = RangeAddresses.fromLabel("A1:B3"),
                workbookKey = WorkbookKeys.fromNameAndPath(""),
                worksheetName = "abc"
            ),
            windowId = None
        )
        proto = o.toProtoObj()
        self.assertEqual(o.errorIndicator.toProtoObj(), proto.errorIndicator)
        self.assertEqual(o.rangeId.toProtoObj(), proto.rangeId)
        self.assertFalse(proto.HasField("windowId"))

    def test_fromProtoBytes(self):
        proto = RangeToClipboardResponseProto(
            errorIndicator = ErrorIndicator.noError().toProtoObj(),
            rangeId = RangeId(
                rangeAddress = RangeAddresses.fromLabel("A1:B3"),
                workbookKey = WorkbookKeys.fromNameAndPath(""),
                worksheetName = "abc"
            ).toProtoObj(),
            windowId = "asd"
        )
        o = RangeToClipboardResponse.fromProtoBytes(proto.SerializeToString())
        self.assertEqual(proto.windowId,o.windowId)
        self.assertEqual(ErrorIndicator.fromProto(proto.errorIndicator),o.errorIndicator)
        self.assertEqual(RangeId.fromProto(proto.rangeId),o.rangeId)


if __name__ == '__main__':
    unittest.main()
