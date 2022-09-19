import unittest
from unittest.mock import MagicMock

from com.qxdzbc.p6.cell.TestDataCell import TestDataCell
from com.qxdzbc.p6.cell.IndCell import IndCell
from com.qxdzbc.p6.cell.address.CellAddresses import CellAddresses
from com.qxdzbc.p6.proto.DocProtos_pb2 import CellProto
from com.qxdzbc.p6.range.address.RangeAddresses import RangeAddresses
from com.qxdzbc.p6.util.for_test import TestUtils
from com.qxdzbc.p6.workbook.key.WorkbookKeys import WorkbookKeys
from com.qxdzbc.p6.rpc.data_structure.BoolMsg import BoolMsg
from com.qxdzbc.p6.cell.rpc_data_structure.CellId import CellId
from com.qxdzbc.p6.cell.rpc_data_structure.CellValue import CellValue
from com.qxdzbc.p6.rpc.data_structure.SingleSignalResponse import \
    SingleSignalResponse
from com.qxdzbc.p6.worksheet.IndWorksheet import IndWorksheet
from com.qxdzbc.p6.worksheet.LoadType import LoadType
from com.qxdzbc.p6.worksheet.RpcWorksheet import RpcWorksheet
from com.qxdzbc.p6.worksheet.rpc_data_structure.CellCountResponse import CellCountResponse
from com.qxdzbc.p6.worksheet.rpc_data_structure.GetAllCellResponse import GetAllCellResponse
from com.qxdzbc.p6.worksheet.rpc_data_structure.GetUsedRangeResponse import GetUsedRangeResponse
import pandas as pd

from com.qxdzbc.p6.worksheet.rpc_data_structure.LoadDataRequest import LoadDataRequest


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
        array3d = [[[1, 2, 3], [4, 5, 6]], [[7, 8, 9], [10, 11, 12]]]
        array2d = [[1, 2, 3], [4, 5, 6]]

        def errCase():
            self.mockWsService.loadData = MagicMock(return_value = SingleSignalResponse().toProtoObj())
            # x: incorrect array dimension
            rs3d = self.ws.load2DArrayRs(array3d)
            self.assertTrue(rs3d.isErr())
            self.mockWsService.loadData.assert_not_called()
            # x: error from rpc server
            self.mockWsService.loadData = MagicMock(
                return_value = SingleSignalResponse(errorReport = TestUtils.TestErrorReport).toProtoObj())
            rsEr = self.ws.load2DArrayRs(array2d)
            self.mockWsService.loadData.assert_called_once()
            self.assertTrue(rsEr.isErr())

        def okCase():
            self.mockWsService.loadData = MagicMock(return_value = SingleSignalResponse().toProtoObj())
            ca = CellAddresses.fromColRow(3, 2)
            lt = LoadType.KEEP_OLD_DATA_IF_COLLIDE
            rs2d = self.ws.load2DArrayRs(array2d, ca, lt)
            self.assertTrue(rs2d.isOk())
            expectedCells = []
            for (r, rowArray) in enumerate(array2d):
                for (c, item) in enumerate(rowArray):
                    expectedCells.append(IndCell(
                        address = CellAddresses.fromColRow(
                            ca.colIndex + c, ca.rowIndex + r
                        ),
                        value = CellValue.fromAny(item)
                    ))
            expectedInput = LoadDataRequest(
                loadType = lt,
                ws = IndWorksheet(
                    id = self.ws.id,
                    cells = expectedCells
                ),
            )
            print(expectedInput.toProtoObj())
            self.mockWsService.loadData.assert_called_with(request = expectedInput.toProtoObj())

        okCase()
        errCase()

    def test_loadDataFrame_incorrect_data_type(self):
        df = 123
        rs = self.ws.loadDataFrameRs(df)
        self.assertTrue(rs.isErr())

    def test_loadDataFrame_incorrect_dimen(self):
        array2d = [[1, 2, 3], [4, 5, 6]]
        # each sub array is a column
        df = pd.DataFrame({"a": array2d[0], "b": array2d[1]})
        # each sub array is a row

        df2 = pd.DataFrame(array2d)
        # pandas data loop by column, not by row

        ca = CellAddresses.fromColRow(33, 22)
        lt = LoadType.KEEP_OLD_DATA_IF_COLLIDE

        def errCase():
            self.mockWsService.loadData = MagicMock(
                return_value = SingleSignalResponse(errorReport = TestUtils.TestErrorReport).toProtoObj())
            df = "not a data frame"
            rs = self.ws.loadDataFrameRs(df, ca, lt)
            self.mockWsService.loadData.assert_not_called()
            self.assertTrue(rs.isErr())

        def okCase():
            df = pd.DataFrame(array2d)
            self.mockWsService.loadData = MagicMock(return_value = SingleSignalResponse().toProtoObj())
            cpmList = []
            for ci in df:
                for (i, item) in enumerate(df[ci]):
                    cpm = IndCell(
                        address = CellAddresses.fromColRow(
                            ca.colIndex + ci, ca.rowIndex + i
                        ),
                        value = CellValue.fromAny(item)
                    )
                    cpmList.append(cpm)
            expectedInput_WithoutHeader = LoadDataRequest(
                loadType = lt,
                ws = IndWorksheet(
                    id = self.ws.id,
                    cells = cpmList
                ),
            )

            rs = self.ws.loadDataFrameRs(df, ca, lt, False)
            self.assertTrue(rs.isOk())
            self.mockWsService.loadData.assert_called_with(request = expectedInput_WithoutHeader.toProtoObj())

            ##########

        def ok_withHeader():
            df = pd.DataFrame(array2d)
            self.mockWsService.loadData = MagicMock(return_value = SingleSignalResponse().toProtoObj())
            headerCpmList = []
            for (i, header) in enumerate(list(df.columns)):
                cpm = IndCell(
                    address = CellAddresses.fromColRow(
                        ca.colIndex + i, ca.rowIndex
                    ),
                    value = CellValue.fromStr(str(header))
                )
                headerCpmList.append(cpm)

            cpmList = []
            for ci in df:
                for (i, item) in enumerate(df[ci]):
                    cpm = IndCell(
                        address = CellAddresses.fromColRow(
                            ca.colIndex + ci, ca.rowIndex + i + 1
                        ),
                        value = CellValue.fromAny(item)
                    )
                    cpmList.append(cpm)

            expectedInput_Header = LoadDataRequest(
                loadType = lt,
                ws = IndWorksheet(
                    id = self.ws.id,
                    cells = headerCpmList + cpmList
                ),
            )
            rs = self.ws.loadDataFrameRs(df, ca, lt, True)
            self.assertTrue(rs.isOk())
            self.mockWsService.loadData.assert_called_with(request = expectedInput_Header.toProtoObj())

        errCase()
        okCase()
        ok_withHeader()

    def test_containAddress(self):
        self.mockWsService.containAddress = MagicMock(return_value = BoolMsg(True).toProtoObj())
        o = self.ws.containsAddress(CellAddresses.fromLabel("DS2"))
        self.assertTrue(o)

        self.mockWsService.containAddress = MagicMock(return_value = BoolMsg(False).toProtoObj())
        o = self.ws.containsAddress(CellAddresses.fromLabel("DS2"))
        self.assertFalse(o)

    def test_addCell(self):
        cell = TestDataCell(
            address = CellAddresses.fromLabel("B4"),
            wsName = "anyWsName",
            wbKey = WorkbookKeys.fromNameAndPath("anyWbName", None),
            value = 123,
        )
        self.mockWsService.addCell = MagicMock(return_value = SingleSignalResponse().toProtoObj())
        self.ws.addCell(cell)
        self.mockWsService.addCell.assert_called_with(
            request = CellProto(
                id = CellId(
                    cell.address, self.ws.wbKey, self.ws.name
                ).toProtoObj(),
                value = CellValue.fromNum(123).toProtoObj(),
                formula = None
            )
        )

    def test_cells(self):
        cellAddressList = list(map(lambda c: CellAddresses.fromLabel(c), ["A1", "K8", "Q10"]))
        self.mockWsService.getAllCell = MagicMock(return_value = GetAllCellResponse(cellAddressList).toProtoObj())
        c = self.ws.cells
        self.assertEqual(cellAddressList, list(map(lambda c: c.address, c)))

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
        self.mockWsService.getUsedRangeAddress = MagicMock(
            return_value = GetUsedRangeResponse(rangeAddress = r).toProtoObj())
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
