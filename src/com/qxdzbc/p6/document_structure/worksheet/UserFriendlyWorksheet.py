from abc import ABC
from typing import Tuple, Union

from com.qxdzbc.p6.document_structure.cell.address.CellAddress import CellAddress
from com.qxdzbc.p6.document_structure.range.Range import Range
from com.qxdzbc.p6.document_structure.range.address.RangeAddress import RangeAddress


class UserFriendlyWorksheet(ABC):

    """an interface for the end user to use"""

    def range(self, rangeAddress: Union[str, RangeAddress, Tuple[CellAddress, CellAddress]]) -> Range:
        raise NotImplementedError()