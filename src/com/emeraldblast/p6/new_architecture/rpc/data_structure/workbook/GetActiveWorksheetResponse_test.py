import unittest

from com.emeraldblast.p6.document_structure.worksheet.WorksheetImp import WorksheetImp
from com.emeraldblast.p6.new_architecture.rpc.data_structure.workbook.GetActiveWorksheetResponse import \
    GetActiveWorksheetResponse


class GetActiveWorksheetResponse_test(unittest.TestCase):
    def test_from_toProto(self):
        o = GetActiveWorksheetResponse(
            worksheet = WorksheetImp("ws",None)
        )
        p = o.toProtoObj()
        self.assertTrue(p.HasField("worksheet"))
        self.assertEqual(o.worksheet.toProtoObj(),p.worksheet)
        
        o2 = GetActiveWorksheetResponse()
        p2 = o2.toProtoObj()
        self.assertFalse(p2.HasField("worksheet"))
        
        o22 = GetActiveWorksheetResponse.fromProto(p2,None)
        self.assertEqual(o2,o22)


if __name__ == '__main__':
    unittest.main()
