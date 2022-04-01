import unittest

from bicp_document_structure.communication.proto.DocProto_pb2 import CellAddressProto


class ProtoTestBench(unittest.TestCase):
    def test_something(self):
        cellAddress = CellAddressProto()
        cellAddress.row = 123
        cellAddress.col=333
        a2 = CellAddressProto()
        a2.ParseFromString(cellAddress.SerializeToString())
        print(a2)
        print(a2.SerializeToString())
