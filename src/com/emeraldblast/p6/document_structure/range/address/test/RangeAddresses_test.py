import unittest

from com.emeraldblast.p6.document_structure.cell.address.CellIndex import CellIndex
from com.emeraldblast.p6.document_structure.range.address.RangeAddressImp import RangeAddressImp
from com.emeraldblast.p6.document_structure.range.address.RangeAddresses import RangeAddresses
from com.emeraldblast.p6.document_structure.util.result.Err import Err
from com.emeraldblast.p6.document_structure.util.result.Ok import Ok
from com.emeraldblast.p6.document_structure.worksheet.WorksheetConst import WorksheetConst


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

            "@A:A": RangeAddressImp(CellIndex(1, 1), CellIndex(1, WorksheetConst.rowLimit)),
            "@B:B": RangeAddressImp(CellIndex(2, 1), CellIndex(2, WorksheetConst.rowLimit)),
            "@B:F": RangeAddressImp(CellIndex(2, 1), CellIndex(6, WorksheetConst.rowLimit)),
            "@F:B": RangeAddressImp(CellIndex(2, 1), CellIndex(6, WorksheetConst.rowLimit)),
            "@5:5": RangeAddressImp(CellIndex(1, 5), CellIndex(WorksheetConst.colLimit, 5)),
            "@5:10": RangeAddressImp(CellIndex(1, 5), CellIndex(WorksheetConst.colLimit, 10)),
            "@10:5": RangeAddressImp(CellIndex(1, 5), CellIndex(WorksheetConst.colLimit, 10)),
        }

        for k, v in data.items():
            label = RangeAddresses.addressFromLabel(k)
            self.assertEqual(label, v)

    def test_constructorWithMalformedLabel(self):
        with self.assertRaises(ValueError):
            RangeAddresses.addressFromLabel("A1:ABC2")
        with self.assertRaises(ValueError):
            RangeAddresses.addressFromLabel("A1:@ABC2")
        with self.assertRaises(ValueError):
            RangeAddresses.addressFromLabel("@A_1:ABC2")
        with self.assertRaises(ValueError):
            RangeAddresses.addressFromLabel("@_A1:ABC2")
        with self.assertRaises(ValueError):
            RangeAddresses.addressFromLabel("@_A1:_ABC2")
        with self.assertRaises(ValueError):
            RangeAddresses.addressFromLabel("@_A1:_ABC2")
        with self.assertRaises(ValueError):
            RangeAddresses.addressFromLabel("A:L")
        with self.assertRaises(ValueError):
            RangeAddresses.addressFromLabel("1:32")
        with self.assertRaises(ValueError):
            RangeAddresses.addressFromLabel("@A1:A")
        with self.assertRaises(ValueError):
            RangeAddresses.addressFromLabel("@A")
        with self.assertRaises(ValueError):
            RangeAddresses.addressFromLabel("@1")
        with self.assertRaises(ValueError):
            RangeAddresses.addressFromLabel("@A:")
        with self.assertRaises(ValueError):
            RangeAddresses.addressFromLabel(":@A")

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
