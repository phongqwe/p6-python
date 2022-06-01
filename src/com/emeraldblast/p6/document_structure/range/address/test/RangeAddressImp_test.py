import unittest

from com.emeraldblast.p6.document_structure.cell.address.CellAddresses import CellAddresses
from com.emeraldblast.p6.document_structure.cell.address.CellIndex import CellIndex
from com.emeraldblast.p6.document_structure.range.address.RangeAddressImp import RangeAddressImp
from com.emeraldblast.p6.document_structure.range.address.RangeAddresses import RangeAddresses

from com.emeraldblast.p6.proto.DocProtos_pb2 import RangeAddressProto


class RangeAddressImp_test(unittest.TestCase):
    def test_toProto(self):
        topLeft = CellAddresses.fromColRow(1,1)
        botRight = CellAddresses.fromColRow(20,30)
        r = RangeAddressImp(
            topLeft = topLeft,
            botRight = botRight,
        )
        expect = RangeAddressProto()
        expect.topLeft.CopyFrom(topLeft.toProtoObj())
        expect.botRight.CopyFrom(botRight.toProtoObj())
        self.assertEqual(expect,r.toProtoObj())
