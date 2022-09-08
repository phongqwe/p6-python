import unittest

from com.qxdzbc.p6.document_structure.script.ScriptEntryKey import ScriptEntryKey
from com.qxdzbc.p6.document_structure.workbook.key.WorkbookKeys import WorkbookKeys


class ScriptEntryKey_test(unittest.TestCase):
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
