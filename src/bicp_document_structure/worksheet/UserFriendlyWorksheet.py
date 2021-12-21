from abc import ABC
from typing import Tuple, Union

from bicp_document_structure.cell.address.CellAddress import CellAddress
from bicp_document_structure.range.Range import Range
from bicp_document_structure.range.RangeImp import RangeImp
from bicp_document_structure.range.address.RangeAddress import RangeAddress


class UserFriendlyWorksheet(ABC):

    """an interface for the end user to use"""

    def range(self, rangeAddress: Union[str, RangeAddress, Tuple[CellAddress, CellAddress]]) -> Range:
        raise NotImplementedError()
        # parsedAddress = rangeAddress
        # if isinstance(rangeAddress, str):
        #     parsedAddress = RangeLabel(rangeAddress)
        #
        # if isinstance(rangeAddress, Tuple):
        #     ad1 = rangeAddress[0]
        #     ad2 = rangeAddress[1]
        #     parsedAddress = RangeAddressImp(ad1, ad2)

        return RangeImp.fromRangeAddress(parsedAddress, self)
