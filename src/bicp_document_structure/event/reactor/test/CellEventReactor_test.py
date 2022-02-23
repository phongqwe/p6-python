import unittest

from bicp_document_structure.cell.Cell import Cell
from bicp_document_structure.cell.DataCell import DataCell
from bicp_document_structure.cell.address.CellIndex import CellIndex
from bicp_document_structure.event.reactor.CellReactor import CellReactor


class CellEventReactorTest(unittest.TestCase):
    x=0
    def cb(self,cell:Cell):
        self.x+=1
    def test_callbackIsCalled(self):
        cell = DataCell(CellIndex(1,2),)
        cellReactor = CellReactor("123", self.cb)
        cellReactor.react(cell)
        self.assertEqual(1,self.x)