import unittest

from com.qxdzbc.p6.new_architecture.data_structure.app_event import \
    CreateNewWorkbookRequest
from com.qxdzbc.p6.proto.AppEventProtos_pb2 import CreateNewWorkbookRequestProto


class CreateNewWorkbookRequest_test(unittest.TestCase):
    def test_fromProtoBytes(self):
        proto = CreateNewWorkbookRequestProto(windowId="12345")
        o = CreateNewWorkbookRequest.fromProtoBytes(proto.SerializeToString())
        self.assertEqual(proto.windowId, o.windowId)

    def test_fromProtoBytes_noneId(self):
        proto = CreateNewWorkbookRequestProto()
        o = CreateNewWorkbookRequest.fromProtoBytes(proto.SerializeToString())
        self.assertEqual(None, o.windowId)






if __name__ == '__main__':
    unittest.main()
