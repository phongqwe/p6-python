import re

from bicp_document_structure.cell.address.CellAddress import CellAddress
from bicp_document_structure.cell.address.CellAddresses import CellAddresses
from bicp_document_structure.cell.address.CellIndex import CellIndex
from bicp_document_structure.range.address.RangeAddress import RangeAddress
from bicp_document_structure.range.address.RangeAddressImp import RangeAddressImp
from bicp_document_structure.util.result.Err import Err
from bicp_document_structure.util.result.Ok import Ok
from bicp_document_structure.util.result.Result import Result


class RangeAddresses:
    @staticmethod
    def fromArbitraryCells(firstCell: CellAddress, secondCell: CellAddress) -> RangeAddress:
        """accept any 2 cellJsons, regardless of order, then construct a RangeAddress from that"""
        topLeftCell = CellIndex(min(firstCell.colIndex, secondCell.colIndex),
                                min(firstCell.rowIndex, secondCell.rowIndex))
        botRightCell = CellIndex(max(firstCell.colIndex, secondCell.colIndex),
                                 max(firstCell.rowIndex, secondCell.rowIndex))
        return RangeAddressImp(topLeftCell, botRightCell)

    @staticmethod
    def addressFromLabel(label: str) -> RangeAddress:
        checkResult = RangeAddresses.__checkAddressFormat(label)
        if checkResult.isOk():
            bareLabel = label[1:]  # remove @
            cellLabels = bareLabel.split(":")
            cellAddresses = list(map(lambda cLabel: CellAddresses.addressFromLabel("@" + cLabel), cellLabels))
            firstCell = cellAddresses[0]
            lastCell = cellAddresses[1]
            return RangeAddressImp(firstCell, lastCell)
        else:
            raise checkResult.err

    __labelPattern = re.compile("@[a-zA-Z]+[1-9][0-9]*:[a-zA-Z]+[1-9][0-9]*")

    @staticmethod
    def __checkAddressFormat(label: str) -> Result:
        """
        :param label: must be like "@[a-zA-Z][1-9][0-9]*:[a-zA-Z][1-9][0-9]*" eg: "@A1:B10"
        :return: Ok if address is legal, Err with an exception otherwise
        """
        if not isinstance(label, str):
            return Err(ValueError("range label must be a string."))
        else:
            if label.startswith("@"):
                matchResult = RangeAddresses.__labelPattern.fullmatch(label)
                if matchResult is not None:
                    return Ok(None)
                else:
                    return Err(
                        ValueError("Range label \"{cdr}\" does not match the required pattern: {pt}"
                                   .format(cdr=label, pt=str(RangeAddresses.__labelPattern.pattern))))
            else:
                return Err(ValueError("Range label must start with \"@\""))
