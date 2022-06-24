import unittest
from dataclasses import dataclass
from datetime import datetime

import time
from unittest.mock import MagicMock

import numpy as np
import pandas
import pandas as pd
from com.emeraldblast.p6.document_structure.communication.event.data_structure.range_event.RangeCopy import RangeCopy
from pandas import DataFrame, read_clipboard
import pyperclip

from com.emeraldblast.p6.document_structure.cell.CellContentImp import CellContentImp
from com.emeraldblast.p6.document_structure.cell.address.CellAddresses import CellAddresses
from com.emeraldblast.p6.document_structure.range.RangeImp import RangeImp
from com.emeraldblast.p6.document_structure.worksheet.WorksheetImp import WorksheetImp


@dataclass
class A:
    x: int
    v: str | None = "Default v"



class Bench(unittest.TestCase):
    def test_z(self):
        d = {
            1:"1v"
        }

