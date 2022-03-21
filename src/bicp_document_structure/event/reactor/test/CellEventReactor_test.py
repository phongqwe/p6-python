import unittest

from bicp_document_structure.cell.DataCell import DataCell
from bicp_document_structure.cell.address.CellIndex import CellIndex
from bicp_document_structure.event.P6Events import P6Events
from bicp_document_structure.event.reactor.CellReactor import CellReactor
from bicp_document_structure.event.reactor.eventData.CellEventData import CellEventData


class CellEventReactorTest(unittest.TestCase):
    x=0
    def cb(self,cell:CellEventData):
        self.x+=1
    def test_callbackIsCalled(self):
        cell = DataCell(CellIndex(1,2),)
        cellReactor = CellReactor("123", self.cb,P6Events.Cell.UpdateValue)
        cellReactor.react(cell)
        self.assertEqual(1,self.x)