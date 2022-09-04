import unittest

from com.qxdzbc.p6.document_structure.workbook.key.WorkbookKeys import WorkbookKeys
from com.qxdzbc.p6.new_architecture.rpc.data_structure.WorksheetId import WorksheetId


class IdentifyWorksheetMsgProto_test(unittest.TestCase):
    def test_toProto_fromProto(self):
        o = WorksheetId(
            wbKey = WorkbookKeys.fromNameAndPath("qwe"),
            wsName = "Sheet1")

        p = o.toProtoObj()
        self.assertEqual(o.wbKey.toProtoObj(),p.wbKey)
        self.assertEqual(o.wsName,p.wsName)
        self.assertFalse(p.HasField("wsIndex"))

        o2 = WorksheetId(
            wbKey = WorkbookKeys.fromNameAndPath("qwe22"),
            wsIndex=123
        )
        p2 = o2.toProtoObj()
        self.assertEqual(o2.wbKey.toProtoObj(), p2.wbKey)
        self.assertEqual(o2.wsIndex, p2.wsIndex)
        self.assertFalse(p2.HasField("wsName"))

        o22 = WorksheetId.fromProto(p2)
        self.assertEqual(o22,o2)


if __name__ == '__main__':
    unittest.main()
