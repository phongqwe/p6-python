import unittest

from com.qxdzbc.p6.cell.TestDataCell import TestDataCell
from com.qxdzbc.p6.cell.address.CellAddresses import CellAddresses
from com.qxdzbc.p6.range.address.RangeAddresses import RangeAddresses
from com.qxdzbc.p6.workbook.key.WorkbookKeys import WorkbookKeys
from com.qxdzbc.p6.range.rpc_data_structure.RangeCopy import RangeCopy
from com.qxdzbc.p6.range.rpc_data_structure.RangeId import RangeId


class RangeCopy_test(unittest.TestCase):
    def test_toProto(self):
        wbk = WorkbookKeys.fromNameAndPath("B")
        o = RangeCopy(
            rangeId = RangeId(
                rangeAddress = RangeAddresses.fromLabel("B2:H10"),
                wbKey = wbk,
                wsName = "S1"
            ),
            cells = [
                TestDataCell(CellAddresses.fromLabel("B3"), wsName = "S1", wbKey = wbk),
                TestDataCell(CellAddresses.fromLabel("D4"), wsName = "S1", wbKey = wbk),
                TestDataCell(CellAddresses.fromLabel("E4"), wsName = "S1", wbKey = wbk),
            ]
        )
        proto = o.toProtoObj()
        self.assertEqual(o.rangeId.toProtoObj(), proto.id)
        cellProtos = []
        cellProtos.extend(proto.cell)
        self.assertEqual(list(map(lambda c: c.toProtoObj(),o.cells)),cellProtos)

    def test_fromProto(self):
        wbk = WorkbookKeys.fromNameAndPath("B")
        o = RangeCopy(
            rangeId = RangeId(
                rangeAddress = RangeAddresses.fromLabel("B2:H10"),
                wbKey = wbk,
                wsName = "S1"
            ),
            cells = [
                TestDataCell(CellAddresses.fromLabel("B3"), wsName = "S1", wbKey = wbk),
                TestDataCell(CellAddresses.fromLabel("D4"), wsName = "S1", wbKey = wbk),
                TestDataCell(CellAddresses.fromLabel("E4"), wsName = "S1", wbKey = wbk),
            ]
        )
        proto = o.toProtoObj()
        #
        # o2 = RangeCopy.fromProto(proto)
        # self.assertEqual(o,o2)


if __name__ == '__main__':
    unittest.main()
