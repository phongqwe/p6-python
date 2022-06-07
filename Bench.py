import unittest
from datetime import datetime

import time
from unittest.mock import MagicMock

import numpy as np
import pandas
import pandas as pd
from pandas import DataFrame, read_clipboard
import pyperclip

from com.emeraldblast.p6.document_structure.cell.CellContentImp import CellContentImp
from com.emeraldblast.p6.document_structure.cell.address.CellAddresses import CellAddresses
from com.emeraldblast.p6.document_structure.range.RangeImp import RangeImp
from com.emeraldblast.p6.document_structure.worksheet.WorksheetImp import WorksheetImp


class A:
    def __init__(self, x:int):
        self.x = x

    def p(self):
        print(self.x)

class B(A):
    pass

class Bench(unittest.TestCase):
    def test_z(self):

        b = B(123)
        b.p()


        # df = pd.DataFrame(np.random.randn(1000000, 1))

        # df.iloc[:99999] = np.nan
        # sdf = df.astype(pd.SparseDtype("float", np.nan))
        # sdf = df
        # sdf.to_clipboard(index = False, header = None)
        # print('original: {:0.2f} bytes'.format(sdf.memory_usage().sum() / 1e3))
        # z = pandas.read_clipboard(skip_blank_lines=False, header=None)
        # z = pandas.read_csv("z.csv",skip_blank_lines=False, header=None)
        # print('readback: {:0.2f} bytes'.format(z.memory_usage().sum() / 1e3))
        # print(z.shape)
        # print(z)
        # pyperclip.copy("ABC")

        q = True
        print(True)











