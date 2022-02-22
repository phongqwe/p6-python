import unittest

from bicp_document_structure.cell.address.CellAddresses import CellAddresses
from bicp_document_structure.column.ColumnImp import ColumnImp
from bicp_document_structure.column.EventColumn import EventColumn


class EventColumnTest(unittest.TestCase):
    def test_EmitEvent(self):
        col = ColumnImp(1,{})
        self.a = 0
        def cb(cell,event):
            self.a+=1
        eventColumn = EventColumn(col,cb)
        self.assertEqual(0,self.a)
        cell = eventColumn.getOrMakeCell(CellAddresses.addressFromLabel("@A1"))
        cell.value=123
        self.assertEqual(1,self.a)
        self.assertTrue(eventColumn.hasCellAt(cell.address))

        cell2 = eventColumn.getOrMakeCell(CellAddresses.addressFromLabel("@A2"))
        cell2.value="444"
        self.assertEqual(2, self.a)

        cell3 = eventColumn.getOrMakeCell(CellAddresses.addressFromLabel("@A1"))
        cell3.value=789
        self.assertEqual(3, self.a)