import unittest
from pathlib import Path

from com.qxdzbc.p6.new_architecture.data_structure.app_event import \
    LoadWorkbookRequest

from com.qxdzbc.p6.proto.AppEventProtos_pb2 import LoadWorkbookRequestProto


class LoadWorkbookRequest_test(unittest.TestCase):
    def test_fromProtoBytes(self):
        protoBytes = LoadWorkbookRequestProto(path = "a_path",windowId="windowId").SerializeToString()
        o = LoadWorkbookRequest.fromProtoBytes(protoBytes)
        self.assertEqual("a_path", o.path)
        self.assertEqual("windowId", o.windowId)

    def test_absolutePath(self):
        o = LoadWorkbookRequest("path","windowId")
        self.assertEqual(Path("path").absolute(), o.absolutePath)


if __name__ == '__main__':
    unittest.main()
