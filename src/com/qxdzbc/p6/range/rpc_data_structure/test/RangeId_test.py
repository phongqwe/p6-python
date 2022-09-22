import unittest

from com.qxdzbc.p6.range.address.RangeAddresses import RangeAddresses
from com.qxdzbc.p6.workbook.key.WorkbookKeys import WorkbookKeys
from com.qxdzbc.p6.range.rpc_data_structure.RangeId import RangeId


class RangeId_test(unittest.TestCase):
    def test_toProto(self):
        o = RangeId(
            rangeAddress = RangeAddresses.fromLabel("A1:B3"),
            wbKey = WorkbookKeys.fromNameAndPath(""),
            wsName = "abc"
        )
        pt = o.toProtoObj()
        self.assertEqual(o.rangeAddress.toProtoObj(),pt.rangeAddress)
        self.assertEqual(o.wsName, pt.wsName)
        self.assertEqual(o.wbKey.toProtoObj(), pt.wbKey)

    def test_fromProto(self):
        o = RangeId(
            rangeAddress = RangeAddresses.fromLabel("A1:B3"),
            wbKey = WorkbookKeys.fromNameAndPath(""),
            wsName = "abc"
        )
        proto = o.toProtoObj()
        o2 = RangeId.fromProto(proto)
        self.assertEqual(o,o2)

if __name__ == '__main__':
    unittest.main()
