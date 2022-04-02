import unittest
from unittest.mock import MagicMock

from bicp_document_structure.cell.DataCell import DataCell
from bicp_document_structure.cell.EventCell import EventCell
from bicp_document_structure.cell.address.CellIndex import CellIndex
from bicp_document_structure.communication.event.reactor.eventData.CellEventData import CellEventData
from bicp_document_structure.formula_translator.FormulaTranslators import FormulaTranslators
from bicp_document_structure.util.Util import makeGetter
from bicp_document_structure.workbook.key.WorkbookKeys import WorkbookKeys


class EventCellTest(unittest.TestCase):

    def test_toProtoObj(self):
        self.a = 0

        c1 = DataCell(CellIndex(1, 1),
                      MagicMock(),
                      123)
        eventCell = EventCell(c1, MagicMock())

        self.assertEqual(c1.toProtoObj(),eventCell.toProtoObj())

    def test_emitEvent(self):
        self.a=0
        def cb(data:CellEventData):
            self.a=self.a+1

        c1 = DataCell(CellIndex(1, 1),makeGetter(FormulaTranslators.standardWbWs("w1",WorkbookKeys.fromNameAndPath("b1","path1"))),123)
        eventCell = EventCell(c1,cb)
        self.assertEqual(0,self.a)

        eventCell.value=123
        self.assertEqual(1,self.a)

        eventCell.script="abc"
        self.assertEqual(2,self.a)

        eventCell.runScript()
        self.assertEqual(3,self.a)

        eventCell.setScriptAndRun("qqq")
        self.assertEqual(4,self.a)

        eventCell.reRun()
        self.assertEqual(5,self.a)

        eventCell.clearScriptResult()
        self.assertEqual(6, self.a)

