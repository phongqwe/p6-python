import unittest
from unittest.mock import MagicMock

from com.emeraldblast.p6.document_structure.communication.event.P6EventTable import P6EventTable
from com.emeraldblast.p6.document_structure.communication.event.P6EventTableImp import P6EventTableImp
from com.emeraldblast.p6.document_structure.communication.event.P6Events import P6Events
from com.emeraldblast.p6.document_structure.communication.event.data_structure.app_event.CloseWorkbookRequest import \
    CloseWorkbookRequest


class P6EventTable_test(unittest.TestCase):
    def test_something(self):
        table = P6EventTableImp()




        self.assertEqual(
            P6Events.Cell.Update.event,
            table.getEventForClazz(P6Events.Cell.Update.Request)
        )

        self.assertEqual(
            P6Events.Cell.Update.event,
            table.getEventForClazz(P6Events.Cell.Update.Response)
        )

        self.assertEqual(
            P6Events.Cell.MultiUpdate.event,
            table.getEventForClazz(P6Events.Cell.MultiUpdate.Request)
        )

        self.assertEqual(
            P6Events.Cell.MultiUpdate.event,
            table.getEventForClazz(P6Events.Cell.MultiUpdate.Response)
        )

        self.assertEqual(
            P6Events.App.CloseWorkbook.event,
            table.getEventForClazz(P6Events.App.CloseWorkbook.Request)
        )

        self.assertEqual(
            P6Events.App.CloseWorkbook.event,
            table.getEventForClazz(P6Events.App.CloseWorkbook.Response)
        )


if __name__ == '__main__':
    unittest.main()
