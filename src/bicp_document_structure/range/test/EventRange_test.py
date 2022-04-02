import unittest
from unittest.mock import MagicMock

from bicp_document_structure.cell.address.CellAddresses import CellAddresses
from bicp_document_structure.cell.address.CellIndex import CellIndex
from bicp_document_structure.communication.event.reactor.eventData.CellEventData import CellEventData
from bicp_document_structure.range.EventRange import EventRange
from bicp_document_structure.range.RangeImp import RangeImp


class EventRangeTest(unittest.TestCase):

    def test_createEventObjs(self):
        parent = MagicMock()
        firstCell = CellIndex(1, 1)
        lastCell = CellIndex(3, 9)
        r = RangeImp(firstCell, lastCell, parent)

        self.a = 0
        self.b=0
        def ce(cellEventData:CellEventData):
            self.a+=1
        def re(rangeEventData):
            self.b+=1

        er = EventRange(r,ce,re)

        # cells
        oldA = self.a
        for cell in er.cells:
            cell.value=123
        self.assertEqual(oldA + len(er.cells),self.a)

        # reRun
        er.reRun()
        oldA = self.a
        self.assertEqual(1,self.b)
        self.assertEqual(oldA,self.a)

        # getCell
        c1 = er.getCell(CellAddresses.addressFromLabel("@B2"))
        oldA = self.a
        c1.value=123
        self.assertEqual(oldA+1,self.a)

        # getOrMakeCell
        c2 = er.getOrMakeCell(CellAddresses.addressFromLabel("@A3"))
        oldA = self.a
        c2.value = 123
        self.assertEqual(oldA+1,self.a)

        # cell
        c3 = er.cell("@A5")
        oldA = self.a
        c3.value=123
        self.assertEqual(oldA + 1, self.a)




