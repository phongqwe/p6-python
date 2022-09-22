import unittest

from com.qxdzbc.p6.cell.CellContent import CellContent
from com.qxdzbc.p6.cell.IndCell import IndCell
from com.qxdzbc.p6.cell.address.CellAddresses import CellAddresses
from com.qxdzbc.p6.cell.rpc_data_structure.CellValue import CellValue


class IndCell_test(unittest.TestCase):
    def test_toProto(self):
        o = IndCell(
            address = CellAddresses.A1,
            content = CellContent(
                value = CellValue.fromNum(123),
                formula = "qqqq"
            ),
        )
        p = o.toProtoObj()
        self.assertEqual(o.address.toProtoObj(),p.address)
        self.assertEqual(o.content.toProtoObj(),p.content)

        o = IndCell(
            address = CellAddresses.A1,
            content = CellContent.empty()
        )
        p = o.toProtoObj()
        self.assertEqual(o.address.toProtoObj(), p.address)
        self.assertTrue(p.HasField("content"))



if __name__ == '__main__':
    unittest.main()
