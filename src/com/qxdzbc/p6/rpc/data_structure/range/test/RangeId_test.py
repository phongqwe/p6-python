import unittest

from com.qxdzbc.p6.range.address.RangeAddresses import RangeAddresses
from com.qxdzbc.p6.workbook.key.WorkbookKeys import WorkbookKeys
from com.qxdzbc.p6.rpc.data_structure.range.RangeId import RangeId


class RangeId_test(unittest.TestCase):
    def test_toProto(self):
        o = RangeId(
            rangeAddress = RangeAddresses.fromLabel("A1:B3"),
            workbookKey = WorkbookKeys.fromNameAndPath(""),
            worksheetName = "abc"
        )
        pt = o.toProtoObj()
        self.assertEqual(o.rangeAddress.toProtoObj(),pt.rangeAddress)
        self.assertEqual(o.worksheetName, pt.worksheetName)
        self.assertEqual(o.workbookKey.toProtoObj(), pt.workbookKey)

    def test_fromProto(self):
        o = RangeId(
            rangeAddress = RangeAddresses.fromLabel("A1:B3"),
            workbookKey = WorkbookKeys.fromNameAndPath(""),
            worksheetName = "abc"
        )
        proto = o.toProtoObj()
        o2 = RangeId.fromProto(proto)
        self.assertEqual(o,o2)

if __name__ == '__main__':
    unittest.main()
