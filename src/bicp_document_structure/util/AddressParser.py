from typing import Union, Tuple

from bicp_document_structure.cell.address.CellAddress import CellAddress
from bicp_document_structure.cell.address.CellIndex import CellIndex
from bicp_document_structure.cell.address.CellLabel import CellLabel
from bicp_document_structure.range.address.RangeAddress import RangeAddress
from bicp_document_structure.range.address.RangeAddressImp import RangeAddressImp
from bicp_document_structure.range.address.RangeLabel import RangeLabel


class AddressParser:
    @staticmethod
    def parseCellAddress(address: Union[str, CellAddress, Tuple[int, int]])->CellAddress:
        parsedAddress = address
        if isinstance(address, str):
            parsedAddress = CellLabel(address)
        if isinstance(address, Tuple):
            parsedAddress = CellIndex(address[0], address[1])
        return parsedAddress

    @staticmethod
    def parseRangeAddress(rangeAddress: Union[str, RangeAddress, Tuple[CellAddress, CellAddress]])->RangeAddress:
        parsedAddress = rangeAddress
        if isinstance(rangeAddress, str):
            parsedAddress = RangeLabel(rangeAddress)

        if isinstance(rangeAddress, Tuple):
            ad1 = rangeAddress[0]
            ad2 = rangeAddress[1]
            parsedAddress = RangeAddressImp(ad1, ad2)
        return parsedAddress