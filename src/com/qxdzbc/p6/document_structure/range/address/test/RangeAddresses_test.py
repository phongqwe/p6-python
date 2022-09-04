import unittest

from com.qxdzbc.p6.document_structure.app.R import R
from com.qxdzbc.p6.document_structure.cell.address.CellAddresses import CellAddresses
from com.qxdzbc.p6.document_structure.cell.address.CellIndex import CellIndex
from com.qxdzbc.p6.document_structure.range.address.RangeAddressImp import RangeAddressImp
from com.qxdzbc.p6.document_structure.range.address.RangeAddresses import RangeAddresses
from com.qxdzbc.p6.document_structure.util.result.Err import Err
from com.qxdzbc.p6.document_structure.util.result.Ok import Ok
from com.qxdzbc.p6.proto.DocProtos_pb2 import RangeAddressProto


class RangeAddresses_test(unittest.TestCase):
    def test_constructor(self):
        data = {
            "@A1:A2": RangeAddressImp(CellIndex(1, 1), CellIndex(1, 2)),
            "@A2:A1": RangeAddressImp(CellIndex(1, 1), CellIndex(1, 2)),
            "@A1:B3": RangeAddressImp(CellIndex(1, 1), CellIndex(2, 3)),
            "@B3:A1": RangeAddressImp(CellIndex(1, 1), CellIndex(2, 3)),
            "@A3:B1": RangeAddressImp(CellIndex(1, 1), CellIndex(2, 3)),
            "@B1:A3": RangeAddressImp(CellIndex(1, 1), CellIndex(2, 3)),
            "@m32:Ab200": RangeAddressImp(CellIndex(13, 32), CellIndex(28, 200)),
            "@m32:ab200": RangeAddressImp(CellIndex(13, 32), CellIndex(28, 200)),
            "@m32:AB200": RangeAddressImp(CellIndex(13, 32), CellIndex(28, 200)),
            "@M32:ab200": RangeAddressImp(CellIndex(13, 32), CellIndex(28, 200)),

            "@A:A": RangeAddressImp(CellIndex(1, 1), CellIndex(1, R.WorksheetConsts.rowLimit)),
            "@B:B": RangeAddressImp(CellIndex(2, 1), CellIndex(2, R.WorksheetConsts.rowLimit)),
            "@B:F": RangeAddressImp(CellIndex(2, 1), CellIndex(6, R.WorksheetConsts.rowLimit)),
            "@F:B": RangeAddressImp(CellIndex(2, 1), CellIndex(6, R.WorksheetConsts.rowLimit)),
            "@5:5": RangeAddressImp(CellIndex(1, 5), CellIndex(R.WorksheetConsts.colLimit, 5)),
            "@5:10": RangeAddressImp(CellIndex(1, 5), CellIndex(R.WorksheetConsts.colLimit, 10)),
            "@10:5": RangeAddressImp(CellIndex(1, 5), CellIndex(R.WorksheetConsts.colLimit, 10)),
        }

        for k, v in data.items():
            label = RangeAddresses.fromLabel(k)
            self.assertEqual(label, v)

    def test_constructorWithMalformedLabel(self):
        with self.assertRaises(ValueError):
            RangeAddresses.fromLabel("A1:ABC2")
        with self.assertRaises(ValueError):
            RangeAddresses.fromLabel("A1:@ABC2")
        with self.assertRaises(ValueError):
            RangeAddresses.fromLabel("@A_1:ABC2")
        with self.assertRaises(ValueError):
            RangeAddresses.fromLabel("@_A1:ABC2")
        with self.assertRaises(ValueError):
            RangeAddresses.fromLabel("@_A1:_ABC2")
        with self.assertRaises(ValueError):
            RangeAddresses.fromLabel("@_A1:_ABC2")
        with self.assertRaises(ValueError):
            RangeAddresses.fromLabel("A:L")
        with self.assertRaises(ValueError):
            RangeAddresses.fromLabel("1:32")
        with self.assertRaises(ValueError):
            RangeAddresses.fromLabel("@A1:A")
        with self.assertRaises(ValueError):
            RangeAddresses.fromLabel("@A")
        with self.assertRaises(ValueError):
            RangeAddresses.fromLabel("@1")
        with self.assertRaises(ValueError):
            RangeAddresses.fromLabel("@A:")
        with self.assertRaises(ValueError):
            RangeAddresses.fromLabel(":@A")

    def test_checkWholeAddressFormat(self):
        self.assertTrue(isinstance(RangeAddresses.checkWholeAddressFormat("@A:A"), Ok))
        self.assertTrue(isinstance(RangeAddresses.checkWholeAddressFormat("@B:A"), Ok))
        self.assertTrue(isinstance(RangeAddresses.checkWholeAddressFormat("@1:23"), Ok))
        self.assertTrue(isinstance(RangeAddresses.checkWholeAddressFormat("@1:1"), Ok))
        self.assertTrue(isinstance(RangeAddresses.checkWholeAddressFormat("@3:B"), Ok))
        self.assertTrue(isinstance(RangeAddresses.checkWholeAddressFormat("@A:23"), Ok))
        self.assertTrue(isinstance(RangeAddresses.checkWholeAddressFormat("@A1:B2"), Err))
        self.assertTrue(isinstance(RangeAddresses.checkWholeAddressFormat("@A:B2"), Err))
        self.assertTrue(isinstance(RangeAddresses.checkWholeAddressFormat("@A1"), Err))
        self.assertTrue(isinstance(RangeAddresses.checkWholeAddressFormat("@123:"), Err))
        self.assertTrue(isinstance(RangeAddresses.checkWholeAddressFormat("@123"), Err))
        self.assertTrue(isinstance(RangeAddresses.checkWholeAddressFormat("@A1:"), Err))
        self.assertTrue(isinstance(RangeAddresses.checkWholeAddressFormat("@A1:"), Err))

    def test_fromArbitraryCells(self):
        cell1 = CellIndex(99, 88)
        cell2 = CellIndex(1, 2)
        r = RangeAddresses.from2Cells(cell1, cell2)
        expect = RangeAddressImp(cell2, cell1)
        self.assertTrue(r == expect)
        self.assertEqual(r, expect)

    def test_label(self):
        self.assertEqual("@A1:A2", RangeAddresses.fromLabel("@A1:A2").label)
        self.assertEqual("@A:B", RangeAddresses.fromLabel("@A:B").label)
        self.assertEqual("@A:B", RangeAddresses.fromLabel("@B:A").label)
        self.assertEqual("@20:30", RangeAddresses.fromLabel("@20:30").label)
        self.assertEqual("@20:30", RangeAddresses.fromLabel("@30:20").label)
        self.assertEqual("@A:C",
                         RangeAddresses.from2Cells(
                             CellIndex(1,1),
                             CellIndex(3,R.WorksheetConsts.rowLimit)).label)
        self.assertEqual("@3:5",
                         RangeAddresses.from2Cells(
                             CellIndex(1, 3),
                             CellIndex(R.WorksheetConsts.colLimit, 5)).label)

        self.assertEqual("@C:Q",
                         RangeAddresses.from2Cells(
                             CellAddresses.fromLabel("@C1"),
                             CellAddresses.fromLabel("@Q{r}".format(r=str(R.WorksheetConsts.rowLimit)))).label)

    def test_fromProto(self):
        topLeft = CellAddresses.fromColRow(1, 1)
        botRight = CellAddresses.fromColRow(20, 30)
        expect = RangeAddressImp(
            topLeft = topLeft,
            botRight = botRight,
        )
        protoRange = RangeAddressProto()
        protoRange.topLeft.CopyFrom(topLeft.toProtoObj())
        protoRange.botRight.CopyFrom(botRight.toProtoObj())
        self.assertEqual(RangeAddresses.fromProto(protoRange),expect)
