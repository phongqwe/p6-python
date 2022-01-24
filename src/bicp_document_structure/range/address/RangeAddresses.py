import re

from bicp_document_structure.cell.address.CellAddress import CellAddress
from bicp_document_structure.cell.address.CellAddresses import CellAddresses
from bicp_document_structure.cell.address.CellIndex import CellIndex
from bicp_document_structure.range.address.RangeAddress import RangeAddress
from bicp_document_structure.range.address.RangeAddressImp import RangeAddressImp
from bicp_document_structure.util.AlphabetBaseNumberSystem import AlphabetBaseNumberSystem
from bicp_document_structure.util.result.Err import Err
from bicp_document_structure.util.result.Ok import Ok
from bicp_document_structure.util.result.Result import Result
from bicp_document_structure.worksheet.WorksheetConst import WorksheetConst


class RangeAddresses:
    @staticmethod
    def fromArbitraryCells(firstCell: CellAddress, secondCell: CellAddress) -> RangeAddress:
        """accept any 2 cells, regardless of order, then construct a RangeAddress from that"""
        topLeftCell = CellIndex(min(firstCell.colIndex, secondCell.colIndex),
                                min(firstCell.rowIndex, secondCell.rowIndex))
        botRightCell = CellIndex(max(firstCell.colIndex, secondCell.colIndex),
                                 max(firstCell.rowIndex, secondCell.rowIndex))
        return RangeAddressImp(topLeftCell, botRightCell)

    @staticmethod
    def addressFromLabel(label: str) -> RangeAddress:
        isNormalRange = RangeAddresses.checkRangeAddressFormat(label)
        # TODO add code to parse whole col/row into address
        if isNormalRange.isOk():
            bareLabel = label[1:]  # remove @
            cellLabels = bareLabel.split(":")
            cellAddresses = list(map(lambda cLabel: CellAddresses.addressFromLabel("@" + cLabel), cellLabels))
            firstCell = cellAddresses[0]
            lastCell = cellAddresses[1]

            firstCol = min(firstCell.colIndex,lastCell.colIndex)
            firstRow = min(firstCell.rowIndex,lastCell.rowIndex)
            lastCol = max(firstCell.colIndex,lastCell.colIndex)
            lastRow = max(firstCell.rowIndex, lastCell.rowIndex)

            return RangeAddressImp(
                firstAddress=CellIndex(firstCol,firstRow),
                lastAddress=CellIndex(lastCol,lastRow)
            )
        else:
            isWholeRange = RangeAddresses.checkWholeAddressFormat(label)
            if isWholeRange.isOk():
                bareLabel = label[1:]
                parts = bareLabel.split(":")
                firstPart = parts[0]
                secondPart = parts[1]

                firstPartIsCol = RangeAddresses.__singleWholeColAddressPattern.fullmatch(firstPart) is not None
                firstPartIsRow = RangeAddresses.__singleWholeRowAddressPattern.fullmatch(firstPart) is not None

                secondPartIsCol = RangeAddresses.__singleWholeColAddressPattern.fullmatch(secondPart) is not None
                secondPartIsRow = RangeAddresses.__singleWholeRowAddressPattern.fullmatch(secondPart) is not None

                if firstPartIsCol and secondPartIsCol:
                    firstColIndex = AlphabetBaseNumberSystem.toDecimal(firstPart)
                    secondColIndex = AlphabetBaseNumberSystem.toDecimal(secondPart)
                    return RangeAddressImp(
                        firstAddress=CellIndex(min(firstColIndex,secondColIndex),1),
                        lastAddress=CellIndex(max(firstColIndex,secondColIndex),WorksheetConst.rowLimit)
                    )
                elif firstPartIsRow and secondPartIsRow:
                    firstRowIndex = int(firstPart)
                    secondRowIndex = int(secondPart)
                    return RangeAddressImp(
                        firstAddress=CellIndex(1,min(firstRowIndex,secondRowIndex)),
                        lastAddress=CellIndex(WorksheetConst.colLimit,max(firstRowIndex,secondRowIndex))
                    )
                else:
                    raise ValueError("input label \"{lb}\" is not a valid whole column/row address")
            else:
                raise ValueError("input label \"{lb}\" is neither a normal range nor a whole range".format(lb=label))

    __rangeAddressPattern = re.compile("@[a-zA-Z]+[1-9][0-9]*:[a-zA-Z]+[1-9][0-9]*")
    __wholeRangeAddressPattern = re.compile("@([a-zA-Z]+|[1-9][0-9]*):([a-zA-Z]+|[1-9][0-9]*)")
    __singleWholeColAddressPattern = re.compile("[a-zA-Z]+")
    __singleWholeRowAddressPattern = re.compile("[1-9][0-9]*")

    @staticmethod
    def checkWholeAddressFormat(label:str)->Result:
        return RangeAddresses.__checkAddressFormatAgainstPattern(label,RangeAddresses.__wholeRangeAddressPattern)

    @staticmethod
    def checkRangeAddressFormat(label: str) -> Result:
        """
        :param label: must be like "@[a-zA-Z][1-9][0-9]*:[a-zA-Z][1-9][0-9]*" eg: "@A1:B10"
        :return: Ok if address is legal, Err with an exception otherwise
        """
        return RangeAddresses.__checkAddressFormatAgainstPattern(label,RangeAddresses.__rangeAddressPattern)

    @staticmethod
    def __checkAddressFormatAgainstPattern(label: str, pattern) -> Result:
        """
        :param label: must be like "@[a-zA-Z][1-9][0-9]*:[a-zA-Z][1-9][0-9]*" eg: "@A1:B10"
        :return: Ok if address is legal, Err with an exception otherwise
        """
        if not isinstance(label, str):
            return Err(ValueError("range label must be a string."))
        else:
            if label.startswith("@"):
                matchResult = pattern.fullmatch(label)
                if matchResult is not None:
                    return Ok(None)
                else:
                    return Err(
                        ValueError("Range label \"{cdr}\" does not match the required pattern: {pt}"
                                   .format(cdr=label, pt=str(pattern.pattern))))
            else:
                return Err(ValueError("Range label must start with \"@\""))
