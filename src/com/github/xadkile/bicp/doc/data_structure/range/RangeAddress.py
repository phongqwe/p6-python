from com.github.xadkile.bicp.doc.data_structure.cell.address.CellAddress import CellAddress


class RangeAddress:

    def __init__(self,firstAddress:CellAddress, lastAddress:CellAddress):
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
        if isinstance(o,RangeAddress):
            sameFirst = self.firstAddress == o.firstAddress
            sameLast = self.lastAddress == o.lastAddress
            return sameFirst and sameLast
        else:
            return False

