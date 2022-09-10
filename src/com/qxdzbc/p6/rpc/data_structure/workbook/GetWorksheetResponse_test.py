import unittest

from com.qxdzbc.p6.workbook.key.WorkbookKeys import WorkbookKeys
from com.qxdzbc.p6.rpc.data_structure.workbook.GetWorksheetResponse import GetWorksheetResponse
from com.qxdzbc.p6.worksheet.RpcWorksheet import RpcWorksheet
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
