import unittest

from com.qxdzbc.p6.cell.address.CellAddresses import CellAddresses
from com.qxdzbc.p6.rpc.data_structure.cell.CellUpdateContent import \
    CellUpdateContent
from com.qxdzbc.p6.rpc.data_structure.cell.CellUpdateEntry import \
    CellUpdateEntry
from com.qxdzbc.p6.proto.CellProtos_pb2 import CellUpdateContentProto, CellUpdateEntryProto


class CellUpdateEntry_test(unittest.TestCase):

    def setUp(self) -> None:
        super().setUp()
        contentProto = CellUpdateContentProto()
        contentProto.formula = "formula_123"
        contentProto.literal = "literal_abc"
        self.contentProto = contentProto
        self.proto = CellUpdateEntryProto()
        self.proto.content.CopyFrom(contentProto)
        self.addr= CellAddresses.fromLabel("Q12")
        self.proto.cellAddress.CopyFrom(self.addr.toProtoObj())


    def test_fromProto(self):
        c = CellUpdateEntry.fromProto(self.proto)
        self.assertEqual(self.addr, c.cellAddress)
        self.assertEqual(CellUpdateContent.fromProto(self.contentProto), c.content)



if __name__ == '__main__':
    unittest.main()
