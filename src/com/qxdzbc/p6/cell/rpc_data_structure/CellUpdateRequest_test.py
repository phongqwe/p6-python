import unittest

from com.qxdzbc.p6.cell.CellContent import CellContent
from com.qxdzbc.p6.cell.address.CellAddresses import CellAddresses
from com.qxdzbc.p6.cell.rpc_data_structure.CellId import CellId
from com.qxdzbc.p6.cell.rpc_data_structure.CellValue import CellValue
from com.qxdzbc.p6.workbook.key.WorkbookKeys import WorkbookKeys
from com.qxdzbc.p6.cell.rpc_data_structure.CellUpdateRequest import \
    CellUpdateRequest
from com.qxdzbc.p6.proto.CellProtos_pb2 import CellUpdateRequestProto


class CellUpdateRequest_test(unittest.TestCase):
    def test_toProto(self):
        o = CellUpdateRequest(
            cellId = CellId(
                cellAddress = CellAddresses.fromLabel("Q2"),
                wbKey = WorkbookKeys.fromNameAndPath("wb1"),
                wsName = "s1"
            ),
            cellContent = CellContent(
                value = CellValue(vNum = 123),
                formula = "formula 123"
            )
        )
        p = o.toProtoObj()
        self.assertEqual(o.cellId.toProtoObj(),p.cellId)
        self.assertEqual(o.cellContent.toProtoObj(),p.cellContent)



    # def test_fromProto(self):
    #     proto = CellUpdateRequestProto(
    #         workbookKey = WorkbookKeys.fromNameAndPath("b1","/home/abc/Documents/gits/project2/p6/b1.txt").toProtoObj(),
    #         worksheetName = "Sheet1",
    #         cellAddress = CellAddresses.fromLabel("B4").toProtoObj(),
    #         value=b'123',
    #         formula=None
    #     )
    #     o = CellUpdateRequest.fromProto(proto)


if __name__ == '__main__':
    unittest.main()
