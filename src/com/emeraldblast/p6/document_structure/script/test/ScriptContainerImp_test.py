import unittest
from unittest.mock import MagicMock

from com.emeraldblast.p6.document_structure.script.ScriptContainerImp import ScriptContainerImp
from com.emeraldblast.p6.document_structure.script.ScriptEntry import ScriptEntry
from com.emeraldblast.p6.document_structure.script.ScriptEntryKey import ScriptEntryKey
from com.emeraldblast.p6.document_structure.workbook.key.WorkbookKeys import WorkbookKeys


class ScriptContainerImp_test(unittest.TestCase):

    def setUp(self) -> None:
        super().setUp()
        self.wbk1 = WorkbookKeys.fromNameAndPath("wbk1")
        self.wbk2 = WorkbookKeys.fromNameAndPath("wbk2")
        self.cont = ScriptContainerImp()
        self.entries = list(map(lambda s: ScriptEntry(
            key = ScriptEntryKey(s),
            script = s + "script"), ["sk1", "sk2", "sk3"]))

        self.wb1Entries = list(map(
            lambda e: ScriptEntry(
                key = ScriptEntryKey(e, workbookKey = self.wbk1),
                script = f"{e} script"
            ),
            ["wbe1", "wbe2", "wbe3"]
        ))

        self.wb2Entries = list(map(
            lambda e: ScriptEntry(
                key = ScriptEntryKey(e, workbookKey = self.wbk2),
                script = f"{e} script"
            ),
            ["z1", "z2", "z3"]
        ))

        self.cont.addScript(self.entries[0])
        for e in self.wb1Entries:
            self.cont.addScript(e)
        for e in self.wb2Entries:
            self.cont.addScript(e)

    def test_get_add_script(self):
        self.cont.addScript(self.entries[1])
        e = self.cont.getScript(self.entries[1].key)
        self.assertEqual(self.entries[1], e)

        self.assertIsNone(self.cont.getScript(self.entries[2].key))

    def test_removeScript(self):
        self.assertIsNotNone(self.cont.getScript(self.entries[0].key))
        self.cont.removeScript(self.entries[0].key)
        self.assertIsNone(self.cont.getScript(self.entries[0].key))

        self.assertIsNotNone(self.cont.getScript(self.wb1Entries[0].key))
        self.cont.removeScript(self.wb1Entries[0].key)
        self.assertIsNone(self.cont.getScript(self.wb1Entries[0].key))

    def test_allScript(self):
        l = [self.entries[0], *self.wb1Entries, *self.wb2Entries]
        self.assertEqual(l, self.cont.allScripts)


if __name__ == '__main__':
    unittest.main()
