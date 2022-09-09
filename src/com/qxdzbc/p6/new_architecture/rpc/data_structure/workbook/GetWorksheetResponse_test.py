import unittest

from com.qxdzbc.p6.document_structure.workbook.key.WorkbookKeys import WorkbookKeys
from com.qxdzbc.p6.new_architecture.rpc.data_structure.workbook.GetWorksheetResponse import GetWorksheetResponse
from com.qxdzbc.p6.new_architecture.worksheet.RpcWorksheet import RpcWorksheet
from com.qxdzbc.p6.proto.rpc.workbook.WorkbooKServiceProtos_pb2 import GetWorksheetResponseProto


class GetWorksheetResponse_test(unittest.TestCase):
    def test_fromProto(self):
        w = RpcWorksheet("ws1", WorkbookKeys.fromNameAndPath("wb1"),)
        p = GetWorksheetResponseProto(
            worksheet = w.toProtoObj()
        )
        o = GetWorksheetResponse.fromProto(p)
        self.assertTrue(o.worksheet.compareContent(w))


if __name__ == '__main__':
    unittest.main()
