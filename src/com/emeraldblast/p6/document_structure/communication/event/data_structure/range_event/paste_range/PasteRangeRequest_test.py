import unittest

from com.emeraldblast.p6.document_structure.cell.address.CellAddresses import CellAddresses
from com.emeraldblast.p6.document_structure.communication.event.data_structure.WsWb import WsWb
from com.emeraldblast.p6.document_structure.communication.event.data_structure.range_event.paste_range.PasteRangeRequest import \
    PasteRangeRequest
from com.emeraldblast.p6.document_structure.workbook.key.WorkbookKeys import WorkbookKeys
from com.emeraldblast.p6.proto.RangeProtos_pb2 import PasteRangeRequestProto


class PasteRangeRequest_test(unittest.TestCase):
    def test_fromProto(self):
        proto = PasteRangeRequestProto(
            anchorCell = CellAddresses.fromColRow(1, 2).toProtoObj(),
            wsWb = WsWb(
                workbookKey = WorkbookKeys.fromNameAndPath(""),
                worksheetName = "qwe"
            ).toProtoObj(),
            windowId = "123"
        )
        o = PasteRangeRequest.fromProtoBytes(proto.SerializeToString())
        self.assertEqual(CellAddresses.fromProto(proto.anchorCell), o.anchorCell)
        self.assertEqual(WsWb.fromProto(proto.wsWb), o.wsWb)
        self.assertEqual(proto.windowId, o.windowId)


if __name__ == '__main__':
    unittest.main()
