import unittest
from unittest.mock import MagicMock

from com.emeraldblast.p6.document_structure.communication.event.data_structure.common.ErrorIndicator import \
    ErrorIndicator

from com.emeraldblast.p6.document_structure.communication.event.data_structure.range_event.RangeId import RangeId
from com.emeraldblast.p6.proto.RangeProtos_pb2 import RangeToClipboardResponseProto

from com.emeraldblast.p6.document_structure.cell.address.CellAddresses import CellAddresses
from com.emeraldblast.p6.document_structure.cell.address.CellIndex import CellIndex
from com.emeraldblast.p6.document_structure.communication.event.P6Events import P6Events
from com.emeraldblast.p6.document_structure.communication.event.data_structure.range_event.range_to_clipboard.RangeToClipboardResponse import \
    RangeToClipboardResponse
from com.emeraldblast.p6.document_structure.communication.notifier.eventData.AppEventData import EventData
from com.emeraldblast.p6.document_structure.communication.notifier.eventData.CellEventData import CellEventData
from com.emeraldblast.p6.document_structure.range.EventRange import EventRange
from com.emeraldblast.p6.document_structure.range.RangeImp import RangeImp
from com.emeraldblast.p6.document_structure.util.for_test.TestUtils import sampleWb
from com.emeraldblast.p6.document_structure.workbook.WorkBook import Workbook


class EventRangeTest(unittest.TestCase):

    def test_copyToClipBoard(self):
        wb: Workbook = sampleWb("QWE")

        ws = wb.getWorksheet("Sheet1")
        r = ws.range("@J2:K3")

        def onRangeEvent(eventData: EventData):
            self.assertEqual(P6Events.Range.RangeToClipBoard.event, eventData.event)
            res: RangeToClipboardResponse = RangeToClipboardResponse.fromProtoBytes(eventData.data)
            self.assertEqual(RangeId(
                rangeAddress = r.rangeAddress,
                workbookKey = wb.workbookKey,
                worksheetName = ws.name
            ), res.rangeId)
            self.assertEqual(ErrorIndicator.noError(), res.errorIndicator)
        eventRange = EventRange(
            innerRange = r,
            onCellEvent = MagicMock(),
            onRangeEvent = onRangeEvent)

        eventRange.copyToClipboard()

    def test_createEventObjs(self):
        """event objs == event cells, event """
        wb: Workbook = sampleWb("QWE")
        ws = wb.getWorksheet("Sheet1")
        firstCell = CellIndex(1, 1)
        lastCell = CellIndex(3, 9)
        r = RangeImp(firstCell, lastCell, ws)

        self.a = 0
        self.b = 0

        def ce(cellEventData: EventData):
            self.a += 1

        def re(rangeEventData):
            self.b += 1

        er = EventRange(r, ce, re)

        # cells
        oldA = self.a
        for cell in er.cells:
            cell.value = 123
        self.assertEqual(oldA + len(er.cells), self.a)

        # reRun
        er.reRun()
        oldA = self.a
        self.assertEqual(1, self.b)
        self.assertEqual(oldA, self.a)

        # getCell
        c1 = er.getCell(CellAddresses.fromLabel("@B2"))
        oldA = self.a
        c1.value = 123
        self.assertEqual(oldA + 1, self.a)

        # getOrMakeCell
        c2 = er.getOrMakeCell(CellAddresses.fromLabel("@A3"))
        oldA = self.a
        c2.value = 123
        self.assertEqual(oldA + 1, self.a)

        # cell
        c3 = er.cell("@A5")
        oldA = self.a
        c3.value = 123
        self.assertEqual(oldA + 1, self.a)
