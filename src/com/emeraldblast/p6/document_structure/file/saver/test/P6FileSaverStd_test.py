import os
import unittest
from pathlib import Path

from com.emeraldblast.p6.document_structure.file.saver.P6FileSaverStd import P6FileSaverStd
from com.emeraldblast.p6.document_structure.workbook.WorkBook import Workbook
from com.emeraldblast.p6.document_structure.workbook.WorkbookJson import WorkbookJson


class MockWorkbook(Workbook):
    def toJson(self) -> WorkbookJson:
        return WorkbookJson("mockWorkbook", None,[])


class WorkbookSaverStd_test(unittest.TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.path = Path("abc.txt")

    def test_save(self):
        mockWorkbook = MockWorkbook()
        saver = P6FileSaverStd()
        if self.path.exists():
            os.remove(self.path)
        self.assertFalse(self.path.exists())
        saver.saveRs(mockWorkbook, self.path)
        self.assertTrue(self.path.exists())
        savedFile = open(self.path, "r")
        savedContent = savedFile.read()
        self.assertEqual(
            """{"version": "0", "workbookJson": {"name": "mockWorkbook", "path": null, "worksheets": []}}""",
            savedContent)
        savedFile.close()

    def tearDown(self) -> None:
        super().tearDown()
        os.remove(self.path)


if __name__ == '__main__':
    unittest.main()
