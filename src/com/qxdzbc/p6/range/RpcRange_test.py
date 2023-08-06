import unittest
from unittest.mock import MagicMock

import numpy
import pandas

from com.qxdzbc.p6.cell.CellContent import CellContent
from com.qxdzbc.p6.cell.IndCell import IndCell
from com.qxdzbc.p6.range.RpcRange import RpcRange
from com.qxdzbc.p6.range.address.RangeAddresses import RangeAddresses
from com.qxdzbc.p6.rpc.data_structure.SingleSignalResponse import SingleSignalResponse
from com.qxdzbc.p6.util.for_test import TestUtils
from com.qxdzbc.p6.workbook.key.WorkbookKeys import WorkbookKeys
from com.qxdzbc.p6.worksheet.rpc_data_structure.MultiCellUpdateRequest import MultiCellUpdateRequest


class RpcRange_test(unittest.TestCase):
    def setUp(self) -> None:
        super().setUp()
        mockSP = MagicMock()
        mockWsService = MagicMock()
        # mockWbService = MagicMock()
        mockSP.wsService = mockWsService
        # mockSP.wbService = mockWbService
        self.mockSP = mockSP
        self.mockWsService = mockWsService
        # self.mockWbService = mockWbService
        self.range = RpcRange(
            rangeAddress = RangeAddresses.fromLabel("B3:D5"),
            wsName = "qwe",
            wbKey = WorkbookKeys.fromNameAndPath("wb1"),
            stubProvider = self.mockSP
        )
        self.arr = [
                [1, 2, 3, 4, 5, 6],
                [7, 8, 9, 10, 11, 12]
            ]
        self.df = pandas.DataFrame({
            "a": [14, 15, 16, 17, 18, 19],
            "b": [24, 25, 26, 27, 28, 29],
            "c": [34, 35, 36, 37, 38, 39],
            "d": [44, 45, 46, 47, 48, 49],
        })

    def test_assign(self):
        def okCase():
            self.mockWsService.updateMultiCellContent = MagicMock(
                return_value = SingleSignalResponse().toProtoObj())
            d = self.df
            a = self.arr
            rs = self.range.assignRs(d)
            self.assertTrue(rs.isOk())
            rs = self.range.assignRs(a)
            self.assertTrue(rs.isOk())

            self.range.assign(d)
            self.range.assign(a)

        def errCase():
            self.mockWsService.updateMultiCellContent = MagicMock(
                return_value = SingleSignalResponse(TestUtils.TestErrorReport).toProtoObj())
            d = self.df
            a = self.arr
            rs = self.range.assignRs(d)
            self.assertTrue(rs.isErr())
            rs = self.range.assignRs(a)
            self.assertTrue(rs.isErr())

            rs = self.range.assignRs("qwewqe")
            self.assertTrue(rs.isErr())

            with self.assertRaises(BaseException):
                self.range.assign(d)
            with self.assertRaises(BaseException):
                self.range.assign(a)
            with self.assertRaises(BaseException):
                self.range.assign("qwewqe")


        okCase()
        errCase()

    def test_assignDataFrame(self):
        d = self.df
        def errCase():
            self.mockWsService.updateMultiCellContent = MagicMock(
                return_value = SingleSignalResponse(TestUtils.TestErrorReport).toProtoObj())
            rs = self.range.assignDataFrameRs(d)
            self.assertTrue(rs.isErr())
            self.assertTrue(rs.err.isSameErr(TestUtils.TestErrorReport))

            with self.assertRaises(BaseException):
                self.range.assignDataFrame(d)

        def okCase():
            self.mockWsService.updateMultiCellContent = MagicMock(
                return_value = SingleSignalResponse().toProtoObj())
            rs = self.range.assignDataFrameRs(d)
            self.assertTrue(rs.isOk())
            topLeft = self.range.address.topLeft
            expectedUpdateEntries = []
            for c in range(3):
                for r in range(3):
                    expectedUpdateEntries.append(
                        IndCell(
                            address = topLeft.addCol(c).addRow(r),
                            content = CellContent.fromAny(d.iloc[r, c])
                        )
                    )

            self.mockWsService.updateMultiCellContent.assert_called_with(
                request = MultiCellUpdateRequest(
                    wsId = self.range.wsId,
                    updateEntries = expectedUpdateEntries
                ).toProtoObj()
            )
            # x: not throwing exception
            self.range.assignDataFrameRs(d)

        okCase()
        errCase()

    def test_assign2DArray(self):
        a = self.arr
        def okCase():
            self.mockWsService.updateMultiCellContent = MagicMock(return_value = SingleSignalResponse().toProtoObj())

            rs = self.range.assign2dArrayRs(a)

            self.assertTrue(rs.isOk())
            expectedUpdateEntries = []
            topLeft = self.range.address.topLeft
            for r in range(2):
                for c in range(3):
                    expectedUpdateEntries.append(
                        IndCell(
                            address = topLeft.addCol(c).addRow(r),
                            content = CellContent.fromAny(a[r][c])
                        )
                    )

            self.mockWsService.updateMultiCellContent.assert_called_with(
                request = MultiCellUpdateRequest(
                    wsId = self.range.wsId,
                    updateEntries = expectedUpdateEntries
                ).toProtoObj()
            )

            # not throwing exception:
            self.range.assign2dArray(a)

        def errCase():
            self.mockWsService.updateMultiCellContent = MagicMock(
                return_value = SingleSignalResponse(TestUtils.TestErrorReport).toProtoObj())
            rs = self.range.assign2dArrayRs(a)
            self.assertTrue(rs.isErr())
            with self.assertRaises(BaseException):
                self.range.assign2dArray(a)

        okCase()
        errCase()


if __name__ == '__main__':
    unittest.main()
