import unittest

from com.qxdzbc.p6.document_structure.script.ScriptEntry import ScriptEntry
from com.qxdzbc.p6.document_structure.script.ScriptEntryKey import ScriptEntryKey


class ScriptEntry_test(unittest.TestCase):
    def test_from_to_proto(self):
        o = ScriptEntry(
            key = ScriptEntryKey(
                name="skey",
                workbookKey = None
            ),
            script="123asd"
        )

        p = o.toProtoObj()
        self.assertEqual(o.key.toProtoObj(),p.key)
        self.assertEqual(o.script, p.script)
        
        o2 = ScriptEntry.fromProto(p)
        self.assertEqual(o,o2)


if __name__ == '__main__':
    unittest.main()
