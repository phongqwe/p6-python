import unittest
from datetime import datetime

import time
from unittest.mock import MagicMock

import pandas
from pandas import DataFrame, read_clipboard

from com.emeraldblast.p6.document_structure.cell.CellContentImp import CellContentImp
from com.emeraldblast.p6.document_structure.cell.address.CellAddresses import CellAddresses
from com.emeraldblast.p6.document_structure.range.RangeImp import RangeImp
from com.emeraldblast.p6.document_structure.worksheet.WorksheetImp import WorksheetImp


class A:
    def __init__(self,v):
        self.v=v

class B:
    def __init__(self,a):
        self.a=a

class Bench(unittest.TestCase):
    def test_z(self):
        parent = WorksheetImp("S", None)
        parent.cell((1, 1)).value = 11
        parent.cell((1, 2)).formula = "formula 123"
        parent.cell((4, 6)).script = "script abc"

        rangex = RangeImp(
            firstCellAddress = CellAddresses.fromColRow(1, 1),
            lastCellAddress = CellAddresses.fromColRow(5, 6),
            sourceContainer = parent
        )

        array = rangex.toCopiableArray()
        rangex.copyToClipboard()
        dataFrame = read_clipboard(header=None)
        print(dataFrame)
        for r in range(len(dataFrame)):
            row = dataFrame.iloc[r]
            for c in range(len(row)):
                e = dataFrame.iloc[r,c]
                if not pandas.isna(e):
                    print(e)






