import unittest

from com.emeraldblast.p6.document_structure.cell.address.CellAddresses import CellAddresses
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

    def test_intersect(self):
        r1 = RangeAddressImp(
            topLeft = CellAddresses.fromColRow(1,1),
            botRight = CellAddresses.fromColRow(2000,100),
        )
        r2 = RangeAddressImp(
            topLeft = CellAddresses.fromColRow(20,20),
            botRight = CellAddresses.fromColRow(20,20),
        )
        i12 = r1.intersect(r2)
        self.assertEqual(r2, i12)
        i21 = r2.intersect(r1)
        self.assertEqual(i12,i21)

        # B4:F13
        r3 = RangeAddressImp(
            topLeft = CellAddresses.fromLabel("@B4"),
            botRight = CellAddresses.fromLabel("@F13"),
        )
        # D9:H17
        r4 = RangeAddresses.fromLabel("@D9:H17")

        self.assertEqual(RangeAddresses.fromLabel("@D9:F13"), r3.intersect(r4))
        self.assertEqual(RangeAddresses.fromLabel("@E4:F5"), r3.intersect(RangeAddresses.fromLabel("@E3:G5")))
        self.assertEqual(None, r3.intersect(RangeAddresses.fromLabel("@I4:J10")))
