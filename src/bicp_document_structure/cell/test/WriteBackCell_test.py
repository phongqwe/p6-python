import unittest

from bicp_document_structure.cell.Cell import Cell
from bicp_document_structure.cell.DataCell import DataCell
from bicp_document_structure.cell.WriteBackCell import WriteBackCell
from bicp_document_structure.cell.address.CellIndex import CellIndex
from bicp_document_structure.cell.test.MockContainer import MockCellContainer
from bicp_document_structure.formula_translator.FormulaTranslators import FormulaTranslators
from bicp_document_structure.util.Util import makeGetter
from bicp_document_structure.workbook.key.WorkbookKeys import WorkbookKeys
from bicp_document_structure.worksheet.WorksheetImp import WorksheetImp


class WriteBackCellTest(unittest.TestCase):


    # def setUp(self) -> None:
    #     super().setUp()
    #     self.s = WorksheetImp2(name="s3",translatorGetter = self.transGetter)


    def test_Cell(self):
        def transGetter(name):
            return FormulaTranslators.standardWbWs("s3",WorkbookKeys.fromNameAndPath("book1","path123"))

        s = WorksheetImp(name= "s3", translatorGetter = transGetter)
        code = "x=1;y=x+2;y"
        eValue = 3
        address = CellIndex(1, 1)

        # this is a WriteBackCell
        c: Cell = s.getOrMakeCell(address)
        self.assertTrue(s.isEmpty())

        c.script = code
        self.assertFalse(s.isEmpty())
        anotherC = s.getOrMakeCell(address)
        self.assertEqual(code, c.script)
        self.assertEqual(code, anotherC.script)

        c.runScript(globals())
        self.assertEqual(eValue, c.value)
        self.assertEqual(eValue, anotherC.value)

    def test_wbCell(self):
        cellContainer = MockCellContainer()
        address = CellIndex(1, 1)
        c = WriteBackCell(DataCell(address,makeGetter(FormulaTranslators.mock())), cellContainer)
        self.assertFalse(cellContainer.hasCellAt(address))

        # cell is added when script is changed
        c.script = "x=10;x+1;"
        self.assertTrue(cellContainer.hasCellAt(address))
        cellContainer.removeCell(address)

        # cell is added when value is changed
        c.value = 123
        self.assertTrue(cellContainer.hasCellAt(address))
        cellContainer.removeCell(address)

        # cell is added when setScriptAndRun is called
        c.setScriptAndRun("y=10;y+100;",globals())
        self.assertTrue(cellContainer.hasCellAt(address))
        cellContainer.removeCell(address)

        # cell is add when new formula is set
        c.formula="zzbd"
        self.assertTrue(cellContainer.hasCellAt(address))
        cellContainer.removeCell(address)