import os
import unittest
from pathlib import Path

from bicp_document_structure.file.saver.P6FileSaverStd import P6FileSaverStd
from bicp_document_structure.workbook.WorkBook import Workbook
from bicp_document_structure.workbook.WorkbookJson import WorkbookJson


class MockWorkbook(Workbook):
    def toJson(self) -> WorkbookJson:
        return WorkbookJson("mockWorkbook", [])


class WorkbookSaverStd_test(unittest.TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.path = Path("abc.txt")

    def test_save(self):
        mockWorkbook = MockWorkbook()
        saver = P6FileSaverStd()
        self.assertFalse(self.path.exists())
        saver.save(mockWorkbook, self.path)
        self.assertTrue(self.path.exists())
        savedFile = open(self.path, "r")
        savedContent = savedFile.read()
        self.assertEqual(
            """{"version": "0", "workbookJson": {"name": "mockWorkbook", "worksheets": []}}""",
            savedContent)
        savedFile.close()

    def tearDown(self) -> None:
        super().tearDown()
        os.remove(self.path)


if __name__ == '__main__':
    unittest.main()
