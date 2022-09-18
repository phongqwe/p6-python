from dataclasses import dataclass
from typing import Any

from com.qxdzbc.p6.cell.address.CellAddress import CellAddress


@dataclass
class SimpleDataCell:
    """
    this is not a real cell, simply a class that hold a cell address and a data obj
    """
    cellAddress:CellAddress
    data:Any