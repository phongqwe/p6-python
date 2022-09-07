import unittest
from unittest.mock import MagicMock

from com.qxdzbc.p6.document_structure.cell.CellContent import CellContent
from com.qxdzbc.p6.document_structure.cell.address.CellAddresses import CellAddresses
from com.qxdzbc.p6.document_structure.communication.event.data_structure.SingleSignalResponse import \
    SingleSignalResponse
from com.qxdzbc.p6.document_structure.util.for_test import TestUtils
from com.qxdzbc.p6.document_structure.workbook.key.WorkbookKeys import WorkbookKeys
from com.qxdzbc.p6.new_architecture.rpc.cell.RpcCell import RpcCell
from com.qxdzbc.p6.new_architecture.rpc.cell.msg.CopyCellRequest import CopyCellRequest
from com.qxdzbc.p6.new_architecture.rpc.data_structure.CellId import CellId
from com.qxdzbc.p6.new_architecture.rpc.data_structure.CellValue import CellValue
from com.qxdzbc.p6.new_architecture.rpc.data_structure.StrMsg import StrMsg


class RpcCell_test(unittest.TestCase):
    def setUp(self) -> None:
        super().setUp()
        mockSP = MagicMock()
        mockCellService = MagicMock()
        mockSP.cellService = mockCellService
        self.mockSP = mockSP
        self.mockCellService = mockCellService
        self.cell = RpcCell(
            cellAddress = CellAddresses.fromLabel("A2"),
            wsName = "qwe",
            wbKey = WorkbookKeys.fromNameAndPath("wb1"),
            stubProvider = self.mockSP
        )

    def test_displayValue(self):
        v = "Display value"
        self.mockCellService.getDisplayValue = MagicMock(return_value = StrMsg(v).toProtoObj())
        o = self.cell.displayValue
        self.mockCellService.getDisplayValue.assert_called_with(request=self.cell.id.toProtoObj())
        self.assertEqual(v,o)

    def test_getFormula(self):
        v = "formula 123"
        self.mockCellService.getFormula = MagicMock(return_value = StrMsg(v).toProtoObj())
        o = self.cell.formula
        self.mockCellService.getFormula.assert_called_with(request = self.cell.id.toProtoObj())
        self.assertEqual(v, o)

    def test_getCellValue(self):
        v = CellValue.fromNum(123)
        self.mockCellService.getCellValue = MagicMock(return_value = v.toProtoObj())
        o = self.cell.cellValue
        self.mockCellService.getCellValue.assert_called_with(request = self.cell.id.toProtoObj())
        self.assertEqual(v, o)

    def test_cellContent(self):
        v = CellContent(
            formula = "formula 123",
            value=CellValue.fromNum(123)
        )
        self.mockCellService.getCellContent = MagicMock(return_value = v.toProtoObj())
        o = self.cell.content
        self.mockCellService.getCellContent.assert_called_with(request = self.cell.id.toProtoObj())
        self.assertEqual(v, o)

    def test_copyFrom(self):
        anotherCell = CellId(CellAddresses.fromLabel("Q2"),WorkbookKeys.fromNameAndPath("wb2"),"ws33",)
        v = SingleSignalResponse()
        self.mockCellService.copyFrom = MagicMock(return_value = v.toProtoObj())
        o = self.cell.copyFromRs(anotherCell)
        self.assertTrue(o.isOk())
        self.mockCellService.copyFrom.assert_called_with(
            request=CopyCellRequest(
                fromCell = anotherCell,
                toCell = self.cell.id
            ).toProtoObj()
        )

        v = SingleSignalResponse(errorReport = TestUtils.TestErrorReport)
        self.mockCellService.copyFrom = MagicMock(return_value = v.toProtoObj())
        o = self.cell.copyFromRs(anotherCell)
        self.assertTrue(o.isErr())

        with self.assertRaises(Exception):
            self.cell.copyFrom(anotherCell)


if __name__ == '__main__':
    unittest.main()
