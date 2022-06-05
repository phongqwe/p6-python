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
        f = {}
        print(f.get(None))











