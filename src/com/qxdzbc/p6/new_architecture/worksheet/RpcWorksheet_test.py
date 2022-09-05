import unittest
from unittest.mock import MagicMock

from com.qxdzbc.p6.document_structure.cell.DataCell import DataCell
from com.qxdzbc.p6.document_structure.cell.address.CellAddresses import CellAddresses
from com.qxdzbc.p6.document_structure.communication.event.data_structure.SingleSignalResponse import \
    SingleSignalResponse
from com.qxdzbc.p6.document_structure.range.address.RangeAddresses import RangeAddresses
from com.qxdzbc.p6.document_structure.util.for_test import TestUtils
from com.qxdzbc.p6.document_structure.workbook.key.WorkbookKeys import WorkbookKeys
from com.qxdzbc.p6.new_architecture.rpc.data_structure.Cell2Pr import Cell2Pr
from com.qxdzbc.p6.new_architecture.rpc.data_structure.CellId import CellId
from com.qxdzbc.p6.new_architecture.rpc.data_structure.CellValue import CellValue
from com.qxdzbc.p6.new_architecture.worksheet.msg.CellCountResponse import CellCountResponse
from com.qxdzbc.p6.new_architecture.rpc.data_structure.BoolMsg import  BoolMsg
from com.qxdzbc.p6.new_architecture.worksheet.msg.GetAllCellResponse import GetAllCellResponse
from com.qxdzbc.p6.new_architecture.worksheet.RpcWorksheet import RpcWorksheet


class RpcWorksheet_test(unittest.TestCase):
    def setUp(self) -> None:
        super().setUp()
        mockSP = MagicMock()
        mockWsService = MagicMock()
        mockSP.wsService = mockWsService
        self.mockSP = mockSP
        self.mockWsService = mockWsService
        self.ws = RpcWorksheet(
            name = "qwe",
            wbKey = WorkbookKeys.fromNameAndPath("wb1"),
            stubProvider = self.mockSP
        )

    def test_containAddress(self):
        self.mockWsService.containAddress = MagicMock(return_value=BoolMsg(True).toProtoObj())
        o = self.ws.containsAddress(CellAddresses.fromLabel("DS2"))
        self.assertTrue(o)

        self.mockWsService.containAddress = MagicMock(return_value = BoolMsg(False).toProtoObj())
        o = self.ws.containsAddress(CellAddresses.fromLabel("DS2"))
        self.assertFalse(o)

    def test_addCell(self):
        cell = DataCell(
            address = CellAddresses.fromLabel("B4"),
            value = 123
        )
        self.mockWsService.addCell = MagicMock(return_value = SingleSignalResponse().toProtoObj())
        self.ws.addCell(cell)
        self.mockWsService.addCell.assert_called_with(
            request=Cell2Pr(
                id=CellId(
                    cell.address,self.ws._wbk,self.ws.name
                ),
                value = CellValue(num=123),
                formula = None
            ).toProtoObj()
        )

    def test_cells(self):
        cellAddressList=list(map(lambda c: CellAddresses.fromLabel(c), ["A1", "K8", "Q10"]))
        self.mockWsService.getAllCell = MagicMock(return_value = GetAllCellResponse(cellAddressList).toProtoObj())
        c = self.ws.cells
        self.assertEqual(cellAddressList,list(map(lambda c:c.address,c)))

    def test_pasteRs(self):
        self.mockWsService.paste = MagicMock(return_value = SingleSignalResponse().toProtoObj())
        o = self.ws.pasteRs(CellAddresses.fromLabel("A1"))
        self.assertTrue(o.isOk())

        self.mockWsService.paste = MagicMock(return_value = SingleSignalResponse(TestUtils.TestErrorReport).toProtoObj())
        o = self.ws.pasteRs(CellAddresses.fromLabel("A1"))
        self.assertTrue(o.isErr())

    def test_usedRange(self):
        r = RangeAddresses.fromLabel("A1:B9")
        self.mockWsService.getUsedRangeAddress = MagicMock(return_value = r.toProtoObj())
        usedRangeAddress = self.ws.usedRangeAddress
        self.assertEqual(r, usedRangeAddress)
        self.assertEqual(usedRangeAddress.firstRowIndex, self.ws.minUsedRow)
        self.assertEqual(usedRangeAddress.lastRowIndex, self.ws.maxUsedRow)
        self.assertEqual(usedRangeAddress.firstColIndex, self.ws.minUsedCol)
        self.assertEqual(usedRangeAddress.lastColIndex, self.ws.maxUsedCol)

    def test_sheetCount(self):
        self.mockWsService.getCellCount = MagicMock(return_value = CellCountResponse(123).toProtoObj())
        self.assertEqual(123, self.ws.size)


if __name__ == '__main__':
    unittest.main()
