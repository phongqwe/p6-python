import unittest

from com.qxdzbc.p6.cell.rpc_data_structure.CellUpdateContent import \
    CellUpdateContent
from com.qxdzbc.p6.proto.CellProtos_pb2 import CellUpdateContentProto


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
