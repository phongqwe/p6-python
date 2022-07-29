import unittest

from com.emeraldblast.p6.document_structure.workbook.key.WorkbookKeys import WorkbookKeys
from com.emeraldblast.p6.document_structure.worksheet.WorksheetImp import WorksheetImp
from com.emeraldblast.p6.new_architecture.rpc.data_structure.workbook.AddWorksheetRequest import AddWorksheetRequest


class AddWorksheetRequest_test(unittest.TestCase):
    def test_from_toProto(self):
        o = AddWorksheetRequest(
            wbKey = WorkbookKeys.fromNameAndPath("wb1"),
            worksheet = WorksheetImp("ws1",None)
        )
        p = o.toProtoObj()
        self.assertEqual(o.wbKey.toProtoObj(),p.wbKey)
        self.assertEqual(o.worksheet.toProtoObj(),p.worksheet)
        
        o2 = AddWorksheetRequest.fromProto(p,None)
        self.assertEqual(o.wbKey,o2.wbKey)
        self.assertTrue(o.worksheet.compareContent(o2.worksheet))


if __name__ == '__main__':
    unittest.main()
