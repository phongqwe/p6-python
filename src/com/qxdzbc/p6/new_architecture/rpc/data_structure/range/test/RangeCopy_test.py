import unittest

from com.qxdzbc.p6.document_structure.cell.DataCell import DataCell
from com.qxdzbc.p6.document_structure.cell.address.CellAddresses import CellAddresses
from com.qxdzbc.p6.document_structure.range.address.RangeAddresses import RangeAddresses
from com.qxdzbc.p6.document_structure.workbook.key.WorkbookKeys import WorkbookKeys
from com.qxdzbc.p6.new_architecture.rpc.data_structure.range.RangeCopy import RangeCopy
from com.qxdzbc.p6.new_architecture.rpc.data_structure.range.RangeId import RangeId


class RangeCopy_test(unittest.TestCase):
    def test_toProto(self):
        o = RangeCopy(
            rangeId = RangeId(
                rangeAddress = RangeAddresses.fromLabel("B2:H10"),
                workbookKey = WorkbookKeys.fromNameAndPath("B"),
                worksheetName = "S1"
            ),
            cells = [
                DataCell(CellAddresses.fromLabel("B3")),
                DataCell(CellAddresses.fromLabel("D4")),
                DataCell(CellAddresses.fromLabel("E4")),
            ]
        )
        proto = o.toProtoObj()
        self.assertEqual(o.rangeId.toProtoObj(), proto.id)
        cellProtos = []
        cellProtos.extend(proto.cell)
        self.assertEqual(list(map(lambda c: c.toProtoObj(),o.cells)),cellProtos)

    def test_fromProto(self):
        o = RangeCopy(
            rangeId = RangeId(
                rangeAddress = RangeAddresses.fromLabel("B2:H10"),
                workbookKey = WorkbookKeys.fromNameAndPath("B"),
                worksheetName = "S1"
            ),
            cells = [
                DataCell(CellAddresses.fromLabel("B3")),
                DataCell(CellAddresses.fromLabel("D4")),
                DataCell(CellAddresses.fromLabel("E4")),
            ]
        )
        proto = o.toProtoObj()

        o2 = RangeCopy.fromProto(proto)
        self.assertEqual(o,o2)


if __name__ == '__main__':
    unittest.main()
