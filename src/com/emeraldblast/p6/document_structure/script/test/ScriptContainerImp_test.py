import unittest

from com.emeraldblast.p6.document_structure.script.ScriptContainerErrors import ScriptContainerErrors
from com.emeraldblast.p6.document_structure.script.ScriptContainerImp import ScriptContainerImp


class ScriptContainerImp_test(unittest.TestCase):

    def setUp(self) -> None:
        super().setUp()
        self.cont = ScriptContainerImp()

    def test_addScriptRs(self):
        rs = self.cont.addScriptRs("s1","abc1")
        self.assertTrue(rs.isOk())
        c = rs.value
        self.assertTrue(c.contains("s1"))

        rs2 = c.addScriptRs("s1","qwe")
        self.assertTrue(rs2.isErr())
        err = rs2.err
        self.assertTrue(err.isSameErr(ScriptContainerErrors.ScriptAlreadyExist.header))

    def test_replaceName(self):
        name = "script1"
        name2 = "script2"
        c = "casd"
        self.cont = self.cont.addScript(name,c)
        self.assertIsNone(self.cont.getScript(name2))
        self.cont = self.cont.renameScript(name,name2)
        self.assertEqual(c,self.cont.getScript(name2))

    def test_add_remove_getScript(self):
        name = "script1"
        self.assertIsNone(self.cont.getScript(name))
        self.cont = self.cont.addScript(name,"c1")
        self.assertEqual("c1",self.cont.getScript(name))
        self.assertTrue(self.cont.contains(name))

        self.cont = self.cont.removeScript(name)
        self.assertIsNone(self.cont.getScript(name))
        self.assertFalse(self.cont.contains(name))

        self.assertTrue(self.cont.isEmpty())
        self.cont = self.cont.addScript("zz","ds").addScript("asd","qwe")
        self.assertFalse(self.cont.isEmpty())
        self.cont = self.cont.removeAll()
        self.assertTrue(self.cont.isEmpty())





if __name__ == '__main__':
    unittest.main()
