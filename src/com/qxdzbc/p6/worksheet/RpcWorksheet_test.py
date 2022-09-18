import unittest
from unittest.mock import MagicMock

from com.qxdzbc.p6.cell.DataCell import DataCell
from com.qxdzbc.p6.cell.address.CellAddresses import CellAddresses
from com.qxdzbc.p6.proto.DocProtos_pb2 import CellProto
from com.qxdzbc.p6.range.address.RangeAddresses import RangeAddresses
from com.qxdzbc.p6.util.for_test import TestUtils
from com.qxdzbc.p6.workbook.key.WorkbookKeys import WorkbookKeys
from com.qxdzbc.p6.rpc.data_structure.BoolMsg import BoolMsg
from com.qxdzbc.p6.rpc.data_structure.CellId import CellId
from com.qxdzbc.p6.rpc.data_structure.CellValue import CellValue
from com.qxdzbc.p6.rpc.data_structure.SingleSignalResponse import \
    SingleSignalResponse
from com.qxdzbc.p6.worksheet.RpcWorksheet import RpcWorksheet
from com.qxdzbc.p6.worksheet.rpc_data_structure.CellCountResponse import CellCountResponse
from com.qxdzbc.p6.worksheet.rpc_data_structure.GetAllCellResponse import GetAllCellResponse
from com.qxdzbc.p6.worksheet.rpc_data_structure.GetUsedRangeResponse import GetUsedRangeResponse
import pandas as pd


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

    def test_loadArray(self):
        array3d = [[[1,2,3],[4,5,6]],[[7,8,9],[10,11,12]]]
        array2d = [[1,2,3],[4,5,6]]
        rs3d = self.ws.loadArrayRs(array3d)
        self.assertTrue(rs3d.isErr())
        # rs2d = self.ws.loadArrayRs(array2d)
        l = ["a","b"]
        for (q,w) in enumerate(l):
            print(q)
            print(w)


    def test_loadDataFrame_incorrect_data_type(self):
        df = 123
        rs = self.ws.loadDataFrameRs(df)
        self.assertTrue(rs.isErr())

    def test_loadDataFrame_incorrect_dimen(self):
        df = pd.DataFrame([
            [
                [1, 2, 3], [1, 2, 3]
            ],
        ])

        # print(df.shape)
        # rs = self.ws.loadDataFrameRs(df)
        # self.assertTrue(rs.isErr())

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
            wsName = "anyWsName",
            wbKey = WorkbookKeys.fromNameAndPath("anyWbName",None),
            value = 123,
        )
        self.mockWsService.addCell = MagicMock(return_value = SingleSignalResponse().toProtoObj())
        self.ws.addCell(cell)
        self.mockWsService.addCell.assert_called_with(
            request=CellProto(
                id=CellId(
                    cell.address,self.ws.wbKey,self.ws.name
                ).toProtoObj(),
                value = CellValue.fromNum(123).toProtoObj(),
                formula = None
            )
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

        self.mockWsService.paste = MagicMock(return_value = SingleSignalResponse(
            TestUtils.TestErrorReport).toProtoObj())
        o = self.ws.pasteRs(CellAddresses.fromLabel("A1"))
        self.assertTrue(o.isErr())

    def test_usedRange(self):
        r = RangeAddresses.fromLabel("A1:B9")
        self.mockWsService.getUsedRangeAddress = MagicMock(return_value = GetUsedRangeResponse(rangeAddress = r).toProtoObj())
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
