import unittest

from com.emeraldblast.p6.document_structure.file.P6FileMetaInfo import P6FileMetaInfo
from com.emeraldblast.p6.proto.P6FileProtos_pb2 import P6FileMetaInfoProto


class P6FileMetaInfo_test(unittest.TestCase):
    def test_FromProto(self):
        proto = P6FileMetaInfoProto()
        proto.date = 1234
        v = P6FileMetaInfo.fromProto(proto)
        self.assertEqual(v.date,proto.date)

    def test_FromProtoBytes(self):
        proto = P6FileMetaInfoProto()
        proto.date = 666
        v = P6FileMetaInfo.fromProtoBytes(proto.SerializeToString())
        self.assertEqual(v.date, proto.date)

    def test_toProto(self):
        v = P6FileMetaInfo(2234)
        proto = v.toProtoObj()
        self.assertEqual(proto.date, v.date)

if __name__ == '__main__':
    unittest.main()
