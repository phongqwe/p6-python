from abc import ABC
from typing import Union, Tuple

from com.qxdzbc.p6.document_structure.cell.Cell import Cell
from com.qxdzbc.p6.document_structure.cell.address.CellAddress import CellAddress


class UserFriendlyCellContainer(ABC):

    """an interface for the end user to use"""

    def cell(self, address: Union[str, CellAddress, Tuple[int, int]]) -> Cell:
        raise NotImplementedError()