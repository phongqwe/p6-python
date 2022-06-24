import unittest

from com.emeraldblast.p6.document_structure.util.for_test import TestUtils

from com.emeraldblast.p6.document_structure.file.P6FileContent import P6FileContent
from com.emeraldblast.p6.document_structure.file.P6FileMetaInfo import P6FileMetaInfo
from com.emeraldblast.p6.document_structure.file.ScriptInFile import ScriptInFile
from com.emeraldblast.p6.document_structure.workbook.WorkbookImp import WorkbookImp


class P6FileContent_test(unittest.TestCase):
    def test_toProto(self):
        o = P6FileContent(
            meta = P6FileMetaInfo(date=123),
            wb = WorkbookImp("Book1"),
            scripts = [
                ScriptInFile(
                    "sk1","123adsd"
                ),
                ScriptInFile(
                    "sk2", "123adsd"
                )
            ]
        )
        proto = o.toProtoObj()
        self.assertEqual(o.meta.toProtoObj(), proto.meta)
        self.assertEqual(o.wb.toProtoObj(),proto.workbook)
        self.assertTrue(
            TestUtils.compareList(
                list(map(lambda sc: sc.toProtoObj(), o.scripts)),
                proto.scripts
            )
        )
        o2 = P6FileContent.fromProtoBytes(proto.SerializeToString())
        self.assertEqual(o,o2)


if __name__ == '__main__':
    unittest.main()
