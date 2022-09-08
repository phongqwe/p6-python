import unittest
from unittest.mock import MagicMock

from com.qxdzbc.p6.document_structure.cell.address.CellAddresses import CellAddresses
from com.qxdzbc.p6.document_structure.cell.address.CellIndex import CellIndex
from com.qxdzbc.p6.new_architecture.communication import P6Events
from com.qxdzbc.p6.new_architecture.rpc.data_structure.common.ErrorIndicator import \
    ErrorIndicator
from com.qxdzbc.p6.new_architecture.rpc.data_structure.range_event import RangeId
from com.qxdzbc.p6.new_architecture.data_structure import \
    RangeToClipboardResponse
from com.qxdzbc.p6.new_architecture.communication import EventData
from com.qxdzbc.p6.document_structure.range.EventRange import EventRange
from com.qxdzbc.p6.document_structure.range.RangeImp import RangeImp
from com.qxdzbc.p6.document_structure.util.for_test.TestUtils import sampleWb
from com.qxdzbc.p6.document_structure.workbook.WorkBook import Workbook


class EventRangeTest(unittest.TestCase):

    def test_copyProtoToClipBoard(self):
        wb: Workbook = sampleWb("QWE")

        ws = wb.getWorksheet("Sheet1")
        r = ws.range("J2:K3")

        def onRangeEvent(eventData: EventData):
            self.assertEqual(P6Events.Range.RangeToClipBoard.event, eventData.event)
            res: RangeToClipboardResponse = RangeToClipboardResponse.fromProtoBytes(eventData.data.toProtoBytes())
            self.assertEqual(RangeId(
                rangeAddress = r.rangeAddress,
                workbookKey = wb.workbookKey,
                worksheetName = ws.name
            ), res.rangeId)
            self.assertEqual(ErrorIndicator.noError(), res.errorIndicator)
            print("cb was triggered")
        eventRange = EventRange(
            innerRange = r,
            onCellEvent = MagicMock(),
            onRangeEvent = onRangeEvent)

        eventRange.copyToClipboardAsProto()

    def test_copyFullCSVToClipBoard(self):
        wb: Workbook = sampleWb("QWE")

        ws = wb.getWorksheet("Sheet1")
        r = ws.range("J2:K3")

        def onRangeEvent(eventData: EventData):
            self.assertEqual(P6Events.Range.RangeToClipBoard.event, eventData.event)
            res: RangeToClipboardResponse = RangeToClipboardResponse.fromProtoBytes(eventData.data.toProtoBytes())
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

        eventRange.copyValueDataFrame()

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
        # er.reRun()
        # oldA = self.a
        # self.assertEqual(1, self.b)
        # self.assertEqual(oldA, self.a)

        # getCell
        c1 = er.getCell(CellAddresses.fromLabel("B2"))
        oldA = self.a
        c1.value = 123
        self.assertEqual(oldA + 1, self.a)

        # getOrMakeCell
        c2 = er.getOrMakeCell(CellAddresses.fromLabel("A3"))
        oldA = self.a
        c2.value = 123
        self.assertEqual(oldA + 1, self.a)

        # cell
        c3 = er.cell("A5")
        oldA = self.a
        c3.value = 123
        self.assertEqual(oldA + 1, self.a)
