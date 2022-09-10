import unittest

from com.qxdzbc.p6.workbook.key.WorkbookKeys import WorkbookKeys
from com.qxdzbc.p6.rpc.data_structure.workbook.save_wb.SaveWorkbookRequest import \
    SaveWorkbookRequest
from com.qxdzbc.p6.proto.AppProtos_pb2 import SaveWorkbookRequestProto


class SaveWorkbookRequest_test(unittest.TestCase):
    def test_fromProtoBytes(self):
        wbk = WorkbookKeys.fromNameAndPath("a",None)
        proto = SaveWorkbookRequestProto(
            wbKey = wbk.toProtoObj(),
            path = "qwe"
        )

        o = SaveWorkbookRequest.fromProtoBytes(proto.SerializeToString())
        self.assertEqual(wbk,o.workbookKey)
        self.assertEqual(proto.path, o.path)

if __name__ == '__main__':
    unittest.main()
