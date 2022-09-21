import unittest

from com.qxdzbc.p6.cell.CellContent import CellContent
from com.qxdzbc.p6.cell.address.CellAddresses import CellAddresses
from com.qxdzbc.p6.worksheet.rpc_data_structure.CellUpdateEntry import \
    CellUpdateEntry


class CellUpdateEntry_test(unittest.TestCase):

    def test_toProto(self):
        o = CellUpdateEntry(
            cellAddress = CellAddresses.fromLabel("QT12"),
            content = CellContent.fromAny(123)
        )
        p = o.toProtoObj()
        self.assertEqual(o.cellAddress.toProtoObj(),p.cellAddress)
        self.assertEqual(o.content.toProtoObj(),p.content)
    # def setUp(self) -> None:
    #     super().setUp()
    #     contentProto = CellUpdateContentProto()
    #     contentProto.formula = "formula_123"
    #     contentProto.literal = "literal_abc"
    #     self.contentProto = contentProto
    #     self.proto = CellUpdateEntryProto()
    #     self.proto.content.CopyFrom(contentProto)
    #     self.addr= CellAddresses.fromLabel("Q12")
    #     self.proto.cellAddress.CopyFrom(self.addr.toProtoObj())
    #
    #
    # def test_fromProto(self):
    #     c = CellUpdateEntry.fromProto(self.proto)
    #     self.assertEqual(self.addr, c.cellAddress)
    #     self.assertEqual(CellUpdateContent.fromProto(self.contentProto), c.content)



if __name__ == '__main__':
    unittest.main()
