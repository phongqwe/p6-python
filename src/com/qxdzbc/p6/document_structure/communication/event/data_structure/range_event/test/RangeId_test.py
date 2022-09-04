import unittest

from com.qxdzbc.p6.document_structure.communication.event.data_structure.range_event.RangeId import RangeId
from com.qxdzbc.p6.document_structure.range.address.RangeAddresses import RangeAddresses
from com.qxdzbc.p6.document_structure.workbook.key.WorkbookKeys import WorkbookKeys


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
