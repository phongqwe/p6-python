import unittest
from unittest.mock import MagicMock

from bicp_document_structure.util.result.Ok import Ok
from bicp_document_structure.worksheet.OverrideRenameWorksheet import OverrideRenameWorksheet
from bicp_document_structure.worksheet.WorksheetImp import WorksheetImp


class OverrideRenameWorksheet_test(unittest.TestCase):
    def test_renameRs_withRenameFunction(self):
        self.n1 = None
        self.n2 = None

        def renameFunction(n1, n2):
            self.z = 1
            self.n1 = n1
            self.n2 = n2
            return Ok(None)

        ws = OverrideRenameWorksheet(
            WorksheetImp(translatorGetter = MagicMock(), name = "oldName"),
            renameFunction = renameFunction)
        rs = ws.renameRs("newName")
        self.assertTrue(rs.isOk())
        self.assertEqual("oldName", ws.name, "ws should not be renamed")
        self.assertEqual(1, self.z, "rename function should be called")
        self.assertEqual("oldName", self.n1, "rename function arg 1 is incorrect")
        self.assertEqual("newName", self.n2, "rename function arg 2 is incorrect")


if __name__ == '__main__':
    unittest.main()
