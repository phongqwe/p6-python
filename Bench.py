import unittest
from datetime import datetime

import time
from unittest.mock import MagicMock

import numpy as np
import pandas
import pandas as pd
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
        nRows = 20000
        nCols = 1
        # sArray = pd.arrays.SparseArray([])
        # sArray[1:5]=np.nan
        # arr = np.random.randn(10)
        # arr[2:-2] = np.nan
        # ts = pandas.DataFrame(pd.arrays.SparseArray())
        df = pd.DataFrame(index=range(nRows),columns=range(nCols),
                          dtype = pd.SparseDtype(np.dtype('float'))
                          )
        # df[3:4]=123
        print('sparse : {:0.2f} bytes'.format(df.memory_usage().sum() / 1e3))










