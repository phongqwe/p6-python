import unittest


from com.qxdzbc.p6.workbook.key.WorkbookKeys import WorkbookKeys
from com.qxdzbc.p6.rpc.data_structure.workbook.AddWorksheetRequest import AddWorksheetRequest
from com.qxdzbc.p6.worksheet.RpcWorksheet import RpcWorksheet


class AddWorksheetRequest_test(unittest.TestCase):
    def test_from_toProto(self):
        o = AddWorksheetRequest(
            wbKey = WorkbookKeys.fromNameAndPath("wb1"),
            worksheet = RpcWorksheet("ws1",WorkbookKeys.fromNameAndPath("wb"))
        )
        p = o.toProtoObj()
        self.assertEqual(o.wbKey.toProtoObj(),p.wbKey)
        self.assertEqual(o.worksheet.toProtoObj(),p.worksheet)
        
        o2 = AddWorksheetRequest.fromProto(p)
        self.assertEqual(o.wbKey,o2.wbKey)
        self.assertTrue(o.worksheet.compareContent(o2.worksheet))


if __name__ == '__main__':
    unittest.main()
