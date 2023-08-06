from typing import Union, Tuple

from com.qxdzbc.p6.cell.address.CellAddress import CellAddress
from com.qxdzbc.p6.cell.address.CellAddresses import CellAddresses
from com.qxdzbc.p6.range.address.RangeAddress import RangeAddress
from com.qxdzbc.p6.range.address.RangeAddresses import RangeAddresses


class AddressParser:
    @staticmethod
    def parseCellAddress(address: Union[str, CellAddress, Tuple[int, int]])->CellAddress:
        # parsedAddress = address
        # if isinstance(address, str):
        #     parsedAddress = CellAddresses.fromLabel(address)
        # if isinstance(address, Tuple):
        #     parsedAddress = CellIndex(address[0], address[1])
        # return parsedAddress
        return CellAddresses.parse(address)

    @staticmethod
    def parseRangeAddress(rangeAddress: Union[str, RangeAddress, Tuple[CellAddress, CellAddress]])->RangeAddress:
        return RangeAddresses.parse(rangeAddress)
        # parsedAddress = rangeAddress
        # if isinstance(rangeAddress, str):
        #     parsedAddress = RangeAddresses.fromLabel(rangeAddress)
        #
        # if isinstance(rangeAddress, Tuple):
        #     ad1 = rangeAddress[0]
        #     ad2 = rangeAddress[1]
        #     parsedAddress = RangeAddressImp(ad1, ad2)
        # return parsedAddress