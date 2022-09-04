import unittest
from unittest.mock import MagicMock, call

from com.qxdzbc.p6.document_structure.cell.address.CellAddresses import CellAddresses
from com.qxdzbc.p6.document_structure.communication.event import P6EventTableImp
from com.qxdzbc.p6.document_structure.util.for_test.emu.TestEnvImp import TestEnvImp
from com.qxdzbc.p6.document_structure.worksheet.Worksheet import Worksheet


class EventWorksheet_test_integration(unittest.TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.testEnv = TestEnvImp()
        self.testEnv.startEnv()
        self.b1 = self.testEnv.app.getWorkbook("Book1")
        self.z = False
        self.s1: Worksheet = self.b1.getWorksheet(0)
        self.s2: Worksheet = self.b1.getWorksheet(1)
        self.eventTable = P6EventTableImp.P6EventTableImp.i()

    def test_pasteRange(self):
        cb = MagicMock()
        self.testEnv.notifListener.addReactorCB(
            event = P6EventTableImp.P6Events.Range.PasteRange.event,
            reactorCB = cb
        )
        self.s1.range("@J12:F22").copyToClipboardAsProto()
        self.s1.pasteProtoRs(CellAddresses.fromLabel("@V10"))
        self.s1.pasteProto(CellAddresses.fromLabel("@X10"))
        self.assertEqual(2, cb.call_count)


if __name__ == '__main__':
    unittest.main()
