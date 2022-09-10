import unittest

from com.qxdzbc.p6.document_structure.workbook.key.WorkbookKeys import WorkbookKeys
from com.qxdzbc.p6.new_architecture.rpc.data_structure.workbook.GetWorksheetResponse import GetWorksheetResponse
from com.qxdzbc.p6.new_architecture.worksheet.RpcWorksheet import RpcWorksheet
from com.qxdzbc.p6.proto.WorksheetProtos_pb2 import GetWorksheetResponseProto


class GetWorksheetResponse_test(unittest.TestCase):
    def test_fromProto(self):
        w = RpcWorksheet("ws1", WorkbookKeys.fromNameAndPath("wb1"),)
        p = GetWorksheetResponseProto(
            wsId = w.id.toProtoObj()
        )
        o = GetWorksheetResponse.fromProto(p)
        self.assertEqual(o.wsId, w.id)


if __name__ == '__main__':
    unittest.main()
