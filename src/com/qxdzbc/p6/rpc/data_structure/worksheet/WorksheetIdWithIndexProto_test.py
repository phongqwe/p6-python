import unittest

from com.qxdzbc.p6.workbook.key.WorkbookKeys import WorkbookKeys
from com.qxdzbc.p6.rpc.data_structure.worksheet.WorksheetIdWithIndex import WorksheetIdWithIndex


class IdentifyWorksheetMsgProto_test(unittest.TestCase):
    def test_toProto_fromProto(self):
        o = WorksheetIdWithIndex(
            wbKey = WorkbookKeys.fromNameAndPath("qwe"),
            wsName = "Sheet1")

        p = o.toProtoObj()
        self.assertEqual(o.wbKey.toProtoObj(),p.wbKey)
        self.assertEqual(o.wsName,p.wsName)
        self.assertFalse(p.HasField("wsIndex"))

        o2 = WorksheetIdWithIndex(
            wbKey = WorkbookKeys.fromNameAndPath("qwe22"),
            wsIndex=123
        )
        p2 = o2.toProtoObj()
        self.assertEqual(o2.wbKey.toProtoObj(), p2.wbKey)
        self.assertEqual(o2.wsIndex, p2.wsIndex)
        self.assertFalse(p2.HasField("wsName"))

        o22 = WorksheetIdWithIndex.fromProto(p2)
        self.assertEqual(o22,o2)


if __name__ == '__main__':
    unittest.main()
