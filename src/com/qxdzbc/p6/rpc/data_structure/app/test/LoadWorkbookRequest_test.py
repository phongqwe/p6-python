import unittest
from pathlib import Path

from com.qxdzbc.p6.rpc.data_structure.app.LoadWorkbookRequest import LoadWorkbookRequest
from com.qxdzbc.p6.proto.AppProtos_pb2 import LoadWorkbookRequestProto


class LoadWorkbookRequest_test(unittest.TestCase):
    def test_fromProtoBytes(self):
        protoBytes = LoadWorkbookRequestProto(path = "a_path").SerializeToString()
        o = LoadWorkbookRequest.fromProtoBytes(protoBytes)
        self.assertEqual("a_path", o.path)

    def test_absolutePath(self):
        o = LoadWorkbookRequest("path")
        self.assertEqual(Path("path").absolute(), o.absolutePath)


if __name__ == '__main__':
    unittest.main()
