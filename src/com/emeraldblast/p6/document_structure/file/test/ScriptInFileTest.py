import unittest

from com.emeraldblast.p6.document_structure.file.ScriptInFile import ScriptInFile


class ScriptInFileTest(unittest.TestCase):
    def test_from_to_proto(self):
        o = ScriptInFile(
            name="qwe",
            script = "123adsd"
        )
        p = o.toProtoObj()
        self.assertEqual(o.name, p.name)
        self.assertEqual(o.script, p.script)
        o2 = ScriptInFile.fromProto(p)
        self.assertEqual(o,o2)


if __name__ == '__main__':
    unittest.main()
