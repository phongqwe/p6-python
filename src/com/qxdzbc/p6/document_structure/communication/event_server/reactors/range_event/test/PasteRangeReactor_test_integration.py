import unittest

from com.qxdzbc.p6.document_structure.util.for_test.emu.TestEnvImp import TestEnvImp

from com.qxdzbc.p6.document_structure.copy_paste.copier.Copiers import Copiers

from com.qxdzbc.p6.document_structure.cell.address.CellAddresses import CellAddresses
from com.qxdzbc.p6.document_structure.communication.event.data_structure.WsWb import WsWb
from com.qxdzbc.p6.document_structure.communication.event.data_structure.range_event.paste_range.PasteRangeRequest import \
    PasteRangeRequest
from com.qxdzbc.p6.document_structure.communication.event_server.reactors.range_event.PasteRangeReactor import \
    PasteRangeReactor
from com.qxdzbc.p6.document_structure.util.CommonError import CommonErrors
from com.qxdzbc.p6.document_structure.util.result.Ok import Ok
from com.qxdzbc.p6.document_structure.workbook.key.WorkbookKeys import WorkbookKeys


class PasteRangeReactor_test_integration(unittest.TestCase):

    def setUp(self) -> None:
        super().setUp()
        self.testEnv = TestEnvImp()
        self.testEnv.startEnv()
        self.wb = self.testEnv.app.getWorkbook(0)
        #
        # self.wb = sampleWb("b")
        self.ws = self.wb.getWorksheet(0)
        # self.ws = MagicMock()
        # self.ws.
        def wsGetter(wbkey, wsName):
            return Ok(self.ws)

        self.wsGetter = wsGetter
        self.reactor = PasteRangeReactor(self.wsGetter)

    def test_react_faultyInput(self):
        rs = self.reactor.react(b"asd")
        self.assertTrue(rs.isError)
        rs.errorReport.isSameErr(CommonErrors.ExceptionErrorReport.header)

    def test_react_okInput(self):
        request = PasteRangeRequest(
            anchorCell = CellAddresses.fromColRow(2, 3),  # B3
            wsWb = WsWb(
                workbookKey = WorkbookKeys.fromNameAndPath(""),
                worksheetName = "qwe"
            ),
            windowId = "123"
        )

        self.ws.cell((1,1)).value=11
        self.ws.cell((1,2)).value =12
        self.ws.cell((1,3)).formula="=SUM(A1:A2)"
        Copiers.protoCopier.copyRangeToClipboard(self.ws.range("@A1:A3"))

        self.reactor.react(request.toProtoBytes())

        self.assertEqual(self.ws.cell((2+1-1,3+3-1)).formula,self.ws.cell((1,3)).formula)
        z = self.ws.cell((1,3)).value
        x = self.ws.cell((2+1-1,3+3-1)).value
        print("zxc")
        self.assertEqual(z,x)


if __name__ == '__main__':
    unittest.main()
