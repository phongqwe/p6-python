from bicp_document_structure.cell.address.CellAddress import CellAddress
from bicp_document_structure.cell.address.CellLabel import CellLabel
from bicp_document_structure.range.address.RangeAddress import RangeAddress
from bicp_document_structure.range.address.RangeAddressImp import RangeAddressImp
from bicp_document_structure.util.Util import typeCheck


class RangeLabel(RangeAddress):

    def __init__(self,label:str):
        self.__rangeAddress = RangeLabel.addressFromLabel(label)

    @staticmethod
    def addressFromLabel(label: str) -> RangeAddress:
        typeCheck(label, "label", str)
        cellLabels = label.split(":")
        cellAddresses = list(map(lambda cLabel: CellLabel(cLabel), cellLabels))
        firstCell = cellAddresses[0]
        lastCell = cellAddresses[1]
        return RangeAddressImp(firstCell, lastCell)


    @property
    def firstAddress(self) -> CellAddress:
        return self.__rangeAddress.firstAddress

    @property
    def lastAddress(self) -> CellAddress:
        return self.__rangeAddress.lastAddress

    def rowCount(self) -> int:
        return self.__rangeAddress.rowCount()

    def colCount(self) -> int:
        return self.__rangeAddress.colCount()

    def __eq__(self, o: object) -> bool:
        return self.__rangeAddress.__eq__(o)

    def __str__(self) -> str:
        return self.__rangeAddress.__str__()



