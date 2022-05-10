import unittest

from com.emeraldblast.p6.document_structure.file.P6FileContent import P6FileContent
from com.emeraldblast.p6.document_structure.file.P6FileMetaInfo import P6FileMetaInfo
from com.emeraldblast.p6.document_structure.workbook.WorkBook import Workbook
from com.emeraldblast.p6.document_structure.workbook.WorkbookImp import WorkbookImp


class P6FileContent_test(unittest.TestCase):
    def test_toProto(self):
        o = P6FileContent(
            meta = P6FileMetaInfo(date=123),
            wb = WorkbookImp("Book1")
        )
        proto = o.toProtoObj()
        self.assertEqual(o.meta.toProtoObj(), proto.meta)
        self.assertEqual(o.wb.toProtoObj(),proto.workbook)




if __name__ == '__main__':
    unittest.main()