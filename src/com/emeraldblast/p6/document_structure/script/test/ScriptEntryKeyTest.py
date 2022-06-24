import unittest

from com.emeraldblast.p6.document_structure.script.ScriptEntryKey import ScriptEntryKey
from com.emeraldblast.p6.document_structure.workbook.key.WorkbookKeys import WorkbookKeys


class ScriptEntryKeyTest(unittest.TestCase):
    def test_from_to_proto(self):
        o = ScriptEntryKey(
            name = "qwe",
            workbookKey = WorkbookKeys.fromNameAndPath("wbk")
        )
        p1 = o.toProtoObj()
        self.assertEqual(o.name, p1.name)
        self.assertEqual(o.workbookKey.toProtoObj(), p1.workbookKey)

        o2 = ScriptEntryKey.fromProto(p1)
        self.assertEqual(o, o2)


if __name__ == '__main__':
    unittest.main()
