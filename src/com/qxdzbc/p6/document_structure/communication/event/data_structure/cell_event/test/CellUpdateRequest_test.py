import unittest

from com.qxdzbc.p6.document_structure.cell.address.CellAddresses import CellAddresses
from com.qxdzbc.p6.document_structure.communication.event.data_structure.cell_event.CellUpdateRequest import \
    CellUpdateRequest
from com.qxdzbc.p6.document_structure.workbook.key.WorkbookKeys import WorkbookKeys
from com.qxdzbc.p6.proto.CellProtos_pb2 import CellUpdateRequestProto


class CellUpdateRequest_test(unittest.TestCase):
    def test_fromProto(self):
        proto = CellUpdateRequestProto(
            workbookKey = WorkbookKeys.fromNameAndPath("b1","/home/abc/Documents/gits/project2/p6/b1.txt").toProtoObj(),
            worksheetName = "Sheet1",
            cellAddress = CellAddresses.fromLabel("@B4").toProtoObj(),
            value=b'123',
            formula=None
        )
        o = CellUpdateRequest.fromProto(proto)


if __name__ == '__main__':
    unittest.main()
