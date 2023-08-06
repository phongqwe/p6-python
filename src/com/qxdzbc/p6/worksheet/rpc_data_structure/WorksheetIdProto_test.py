import unittest

from com.qxdzbc.p6.workbook.key.WorkbookKeys import WorkbookKeys
from com.qxdzbc.p6.worksheet.rpc_data_structure.WorksheetId import WorksheetId


class WorksheetIdWithIndex_test(unittest.TestCase):
    def test_toProto_fromProto(self):
        o = WorksheetId(
            wbKey = WorkbookKeys.fromNameAndPath("qwe"),
            wsName = "Sheet1")

        p = o.toProtoObj()
        self.assertEqual(o.wbKey.toProtoObj(),p.wbKey)
        self.assertEqual(o.wsName,p.wsName)

        o22 = WorksheetId.fromProto(p)
        self.assertEqual(o22,o)


if __name__ == '__main__':
    unittest.main()
