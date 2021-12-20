from abc import ABC
from typing import Tuple, Union

from bicp_document_structure.cell.Cell import Cell
from bicp_document_structure.cell.address.CellAddress import CellAddress
from bicp_document_structure.range.Range import Range
from bicp_document_structure.range.address.RangeAddress import RangeAddress


class UserFriendlyWorksheet(ABC):
    """an interface exclusively for front end use"""

    def cell(self, address: Union[str, CellAddress,Tuple[int,int]]) -> Cell:
        """get cell"""
        raise NotImplementedError()

    def range(self, rangeAddress: Union[str, RangeAddress,Tuple[CellAddress,CellAddress]]) -> Range:
        """get a range"""
        raise NotImplementedError()
