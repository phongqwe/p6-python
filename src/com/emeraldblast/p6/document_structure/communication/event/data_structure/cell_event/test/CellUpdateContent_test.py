import unittest

from com.emeraldblast.p6.document_structure.communication.event.data_structure.cell_event.CellUpdateContent import \
    CellUpdateContent

from com.emeraldblast.p6.proto.CellProtos_pb2 import CellUpdateContentProto


class CellUpdateContent_test(unittest.TestCase):
    def test_fromProtoByte(self):
        proto = CellUpdateContentProto()
        proto.formula = "formula_123"
        proto.literal = "literal_abc"
        c = CellUpdateContent.fromProtoBytes(proto.SerializeToString())
        self.assertEqual(proto.formula,c.formula)
        self.assertEqual(proto.literal,c.literal)



if __name__ == '__main__':
    unittest.main()
