import unittest

from com.emeraldblast.p6.document_structure.communication.event.data_structure.cell_event.CellUpdateContent import \
    CellUpdateContent

from com.emeraldblast.p6.document_structure.cell.address.CellAddresses import CellAddresses
from com.emeraldblast.p6.document_structure.communication.event.data_structure.cell_event.CellUpdateEntry import \
    CellUpdateEntry
from com.emeraldblast.p6.proto.CellProtos_pb2 import CellUpdateContentProto, CellUpdateEntryProto


class CellUpdateEntry_test(unittest.TestCase):

    def setUp(self) -> None:
        super().setUp()
        contentProto = CellUpdateContentProto()
        contentProto.formula = "formula_123"
        contentProto.literal = "literal_abc"
        self.contentProto = contentProto
        self.proto = CellUpdateEntryProto()
        self.proto.content.CopyFrom(contentProto)
        self.addr= CellAddresses.fromLabel("@Q12")
        self.proto.cellAddress.CopyFrom(self.addr.toProtoObj())


    def test_fromProto(self):
        c = CellUpdateEntry.fromProto(self.proto)
        self.assertEqual(self.addr, c.cellAddress)
        self.assertEqual(CellUpdateContent.fromProto(self.contentProto), c.content)



if __name__ == '__main__':
    unittest.main()
