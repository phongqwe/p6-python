import ast
import unittest

import pyperclip

from com.emeraldblast.p6.document_structure.communication.event.data_structure.common.ErrorIndicator import \
    ErrorIndicator
from com.emeraldblast.p6.document_structure.communication.event.data_structure.range_event.RangeCopy import RangeCopy
from com.emeraldblast.p6.document_structure.communication.event.data_structure.range_event.RangeId import RangeId
from com.emeraldblast.p6.document_structure.communication.event_server.reactors.range_event.RangeToClipboardReactor import \
    RangeToClipboardReactor
from com.emeraldblast.p6.document_structure.range.address.RangeAddresses import RangeAddresses
from com.emeraldblast.p6.document_structure.util.CommonError import CommonErrors
from com.emeraldblast.p6.document_structure.util.for_test.TestUtils import sampleWb
from com.emeraldblast.p6.document_structure.util.result.Err import Err
from com.emeraldblast.p6.document_structure.util.result.Ok import Ok
from com.emeraldblast.p6.document_structure.workbook.WorkBook import Workbook
from com.emeraldblast.p6.proto.RangeProtos_pb2 import RangeToClipboardRequestProto


class RangeToClipboardReactor_test(unittest.TestCase):

    def setUp(self) -> None:
        self.wb: Workbook = sampleWb("B1")

        def rangeGetter(rangeId: RangeId):
            return Ok(self.wb.getWorksheetRs(rangeId.worksheetName).value.range(rangeId.rangeAddress))

        self.rangeGetter = rangeGetter

    def test_react_okCase(self):
        reactor = RangeToClipboardReactor(rangeGetter = self.rangeGetter)
        rangeId = RangeId(
            workbookKey = self.wb.workbookKey,
            worksheetName = "Sheet1",
            rangeAddress = RangeAddresses.fromLabel("@C1:K5")
        )
        request = RangeToClipboardRequestProto(
            rangeId = rangeId.toProtoObj(),
            windowId = "123"
        )
        rs = reactor.react(
            data = request.SerializeToString()
        )

        self.assertEqual(request.windowId, rs.windowId)
        self.assertEqual(request.rangeId, rs.rangeId.toProtoObj())
        self.assertEqual(ErrorIndicator.noError(), rs.errorIndicator)

        targetRange: RangeCopy = self.rangeGetter(rangeId).value.toRangeCopy()
        df = pyperclip.paste()
        clipboardBytes = ast.literal_eval(df)
        self.assertEqual(targetRange.toProtoBytes(), clipboardBytes)

    def test_react_errorCase(self):
        err = CommonErrors.CommonError

        def rangeGetter(rangeId: RangeId):
            return Err(err)

        rangeId = RangeId(
            workbookKey = self.wb.workbookKey,
            worksheetName = "Sheet1",
            rangeAddress = RangeAddresses.fromLabel("@C1:K5")
        )

        reactor = RangeToClipboardReactor(rangeGetter = rangeGetter)
        request = RangeToClipboardRequestProto(
            rangeId=rangeId.toProtoObj(),
        )
        rs = reactor.react(
            data = request.SerializeToString()
        )
        self.assertEqual(None, rs.windowId)
        self.assertEqual(request.rangeId, rs.rangeId.toProtoObj())
        self.assertEqual(ErrorIndicator.error(err), rs.errorIndicator)


if __name__ == '__main__':
    unittest.main()
