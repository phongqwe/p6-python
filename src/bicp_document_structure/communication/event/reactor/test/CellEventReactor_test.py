import unittest

from bicp_document_structure.cell.DataCell import DataCell
from bicp_document_structure.cell.address.CellIndex import CellIndex
from bicp_document_structure.communication.event.reactor.CellReactor import CellReactor
from bicp_document_structure.communication.event.reactor.eventData.CellEventData import CellEventData


class CellEventReactorTest(unittest.TestCase):
    x=0
    def cb(self,cell:CellEventData):
        self.x+=1
    def test_callbackIsCalled(self):
        cell = DataCell(CellIndex(1,2),)
        cellReactor = CellReactor("123", self.cb)
        cellReactor.react(cell)
        self.assertEqual(1,self.x)