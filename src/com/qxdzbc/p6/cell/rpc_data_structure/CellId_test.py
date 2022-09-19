import unittest

from com.qxdzbc.p6.cell.address.CellAddresses import CellAddresses
from com.qxdzbc.p6.workbook.key.WorkbookKeys import WorkbookKeys
from com.qxdzbc.p6.cell.rpc_data_structure.CellId import CellId


class CellId_test(unittest.TestCase):
    def test_from_to_proto(self):
        o = CellId(
            cellAddress = CellAddresses.fromLabel("M2"),
            wbKey = WorkbookKeys.fromNameAndPath("wb1",None),
            wsName = "S1"
        )
        p = o.toProtoObj()
        self.assertEqual(o.wbKey.toProtoObj(),p.wbKey)
        self.assertEqual(o.wsName,p.wsName)
        self.assertEqual(o.cellAddress.toProtoObj(),p.cellAddress)

        o2 = CellId.fromProto(p)
        self.assertEqual(o,o2)


if __name__ == '__main__':
    unittest.main()
