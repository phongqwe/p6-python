from bicp_document_structure.cell.address.CellAddress import CellAddress
from bicp_document_structure.cell.address.CellIndex import CellIndex
from bicp_document_structure.range.address.RangeAddress import RangeAddress
from bicp_document_structure.util.Util import typeCheck


class RangeAddressImp(RangeAddress):

    def __init__(self,firstAddress:CellAddress, lastAddress:CellAddress):
        typeCheck(firstAddress,"firstAddress",CellAddress)
        typeCheck(lastAddress,"lastAddress",CellAddress)
        self.__firstAddress = None
        self.__lastAddress = None
        rowOk = firstAddress.rowIndex <= lastAddress.rowIndex
        colOk = firstAddress.colIndex <= lastAddress.colIndex
        if rowOk and colOk:
            self.__firstAddress = firstAddress
            self.__lastAddress = lastAddress
        else:
            o = "col"
            if not rowOk:
                o = "row"
            reason = "firstAddress {o} is larger than lastAddress {o}".format(o=o)
            raise ValueError("invalid firstAddress and lastAddress: {reason}".format(reason=reason))

    @staticmethod
    def fromArbitraryCells(firstCell:CellAddress, secondCell:CellAddress)->RangeAddress:
        """accept any 2 cellJsons, regardless of order, then construct a RangeAddress from that"""
        topLeftCell = CellIndex(min(firstCell.colIndex, secondCell.colIndex),
                                min(firstCell.rowIndex, secondCell.rowIndex))
        botRightCell = CellIndex(max(firstCell.colIndex, secondCell.colIndex),
                                 max(firstCell.rowIndex, secondCell.rowIndex))
        return RangeAddressImp(topLeftCell,botRightCell)


    @property
    def firstAddress(self)->CellAddress:
        return self.__firstAddress

    @property
    def lastAddress(self)->CellAddress:
        return self.__lastAddress

    def rowCount(self)->int:
        return self.lastAddress.rowIndex - self.firstAddress.rowIndex + 1

    def colCount(self)->int:
        return self.lastAddress.colIndex - self.firstAddress.colIndex + 1

    def __str__(self) -> str:
        return "[{fc}:{lc}]".format(fc=str(self.firstAddress), lc=str(self.lastAddress))

    def __eq__(self, o: object) -> bool:
        if isinstance(o, RangeAddressImp):
            sameFirst = self.firstAddress == o.firstAddress
            sameLast = self.lastAddress == o.lastAddress
            return sameFirst and sameLast
        else:
            return False

