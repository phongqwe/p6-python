import unittest

from com.qxdzbc.p6.document_structure.cell.address.CellAddresses import CellAddresses
from com.qxdzbc.p6.document_structure.range.address.RangeAddressImp import RangeAddressImp
from com.qxdzbc.p6.document_structure.range.address.RangeAddresses import RangeAddresses
from com.qxdzbc.p6.proto.DocProtos_pb2 import RangeAddressProto


class RangeAddressImp_test(unittest.TestCase):

    def test_shiftTopLeftTo(self):
        topLeft = CellAddresses.fromLabel("@B7")
        botRight = CellAddresses.fromLabel("@J10")
        r = RangeAddressImp(
            topLeft = topLeft,
            botRight = botRight,
        )

        r2 = r.moveByTopLeftTo(CellAddresses.fromLabel("@A1"))
        self.assertEqual(RangeAddresses.fromLabel("@A1:I4"),r2)

        r3 = r2.moveByTopLeftTo(CellAddresses.fromLabel("@C9"))
        self.assertEqual(RangeAddresses.fromLabel("@C9:K12"), r3)


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
