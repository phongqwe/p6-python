import unittest

from com.qxdzbc.p6.cell.IndCell import IndCell
from com.qxdzbc.p6.cell.address.CellAddresses import CellAddresses
from com.qxdzbc.p6.rpc.data_structure.CellValue import CellValue


class IndCell_test(unittest.TestCase):
    def test_toProto(self):
        o = IndCell(
            address = CellAddresses.A1,
            value = CellValue.fromNum(123),
            formula="qqqq"
        )
        p = o.toProtoObj()
        self.assertEqual(o.address.toProtoObj(),p.address)
        self.assertEqual(o.value.toProtoObj(),p.value)
        self.assertEqual(o.formula,p.formula)

        o = IndCell(
            address = CellAddresses.A1,
        )
        p = o.toProtoObj()
        self.assertEqual(o.address.toProtoObj(), p.address)
        self.assertFalse(p.HasField("formula"))
        self.assertFalse(p.HasField("value"))



if __name__ == '__main__':
    unittest.main()
