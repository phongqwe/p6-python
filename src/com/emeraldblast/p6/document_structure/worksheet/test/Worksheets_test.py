import unittest
from unittest.mock import MagicMock

from com.emeraldblast.p6.document_structure.cell.CellJson import CellJson
from com.emeraldblast.p6.document_structure.cell.address.CellAddressJson import CellAddressJson
from com.emeraldblast.p6.document_structure.formula_translator.FormulaTranslators import FormulaTranslators
from com.emeraldblast.p6.document_structure.worksheet.Worksheet import Worksheet
from com.emeraldblast.p6.document_structure.worksheet.WorksheetJson import WorksheetJson
from com.emeraldblast.p6.document_structure.worksheet.Worksheets import Worksheets


class Worksheets_test(unittest.TestCase):
    """
    if I hold json object directly, deserialize will be hard.
    """
    @staticmethod
    def transGetter(name):
        return FormulaTranslators.mock()
    def test_something(self):
        json = WorksheetJson(
            name="sheet1",
            cells=[
                CellJson("value1","script1","formula1",CellAddressJson(1,2)),
                CellJson("value2", "script2", "formula2", CellAddressJson(2,3)),
                CellJson("value3", "script3", "formula3", CellAddressJson(3,4))
            ]
        )
        sheet = Worksheets.wsFromJson(json,workbook = MagicMock())
        self.assertTrue(isinstance(sheet,Worksheet))
        self.assertEqual(json.name,sheet.name)
        # cell12 = sheet.cell((1,2))
        # self.assertEqual()



if __name__ == '__main__':
    unittest.main()
