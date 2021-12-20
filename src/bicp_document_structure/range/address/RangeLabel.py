import re

from bicp_document_structure.cell.address.CellAddress import CellAddress
from bicp_document_structure.cell.address.CellLabel import CellLabel
from bicp_document_structure.range.address.RangeAddress import RangeAddress
from bicp_document_structure.range.address.RangeAddressImp import RangeAddressImp
from bicp_document_structure.util.result.Err import Err
from bicp_document_structure.util.result.Ok import Ok
from bicp_document_structure.util.result.Result import Result


class RangeLabel(RangeAddress):
    __labelPattern = re.compile("@[a-zA-Z]+[1-9][0-9]*:[a-zA-Z]+[1-9][0-9]*")

    def __init__(self, label: str):
        self.__rangeAddress = RangeLabel.__addressFromLabel(label)

    @staticmethod
    def __addressFromLabel(label: str) -> RangeAddress:
        checkResult = RangeLabel.__checkAddressFormat(label)
        if checkResult.isOk():
            bareLabel = label[1:]  # remove @
            cellLabels = bareLabel.split(":")
            cellAddresses = list(map(lambda cLabel: CellLabel("@"+cLabel), cellLabels))
            firstCell = cellAddresses[0]
            lastCell = cellAddresses[1]
            return RangeAddressImp(firstCell, lastCell)
        else:
            raise checkResult.err

    @staticmethod
    def __checkAddressFormat(label: str) -> Result:
        """
        check label format
        :param label: must be like "@[a-zA-Z][1-9][0-9]*:[a-zA-Z][1-9][0-9]*" eg: "@A1:B10"
        :return: Ok if address is legal, Err with an exception otherwise
        """
        if not isinstance(label, str):
            return Err(ValueError("range label must be a string."))
        else:
            if label.startswith("@"):
                matchResult = RangeLabel.__labelPattern.fullmatch(label)
                if matchResult is not None:
                    return Ok(None)
                else:
                    return Err(
                        ValueError("Range label \"{cdr}\" does not match the required pattern".format(cdr=label)))
            else:
                return Err(ValueError("Range label must start with \"@\""))

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
