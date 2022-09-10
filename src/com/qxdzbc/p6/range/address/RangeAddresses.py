import re
from typing import Union, Tuple

from com.qxdzbc.p6.app.R import R
from com.qxdzbc.p6.cell.address.CellAddress import CellAddress
from com.qxdzbc.p6.cell.address.CellAddresses import CellAddresses
from com.qxdzbc.p6.cell.address.CellIndex import CellIndex
from com.qxdzbc.p6.range.address.RangeAddress import RangeAddress
from com.qxdzbc.p6.range.address.RangeAddressImp import RangeAddressImp
from com.qxdzbc.p6.util.AlphabetBaseNumberSystem import AlphabetBaseNumberSystem
from com.qxdzbc.p6.util.report.error.ErrorReport import ErrorReport
from com.qxdzbc.p6.util.result.Err import Err
from com.qxdzbc.p6.util.result.Ok import Ok
from com.qxdzbc.p6.util.result.Result import Result
from com.qxdzbc.p6.proto.DocProtos_pb2 import RangeAddressProto


class RangeAddresses:

    @staticmethod
    def fromProtoBytes(protoBytes:bytes)->'RangeAddress':
        proto = RangeAddressProto()
        proto.ParseFromString(protoBytes)
        return RangeAddresses.fromProto(proto)

    @staticmethod
    def fromProto(proto:RangeAddressProto)->'RangeAddress':
        topLeft = CellAddresses.fromProto(proto.topLeft)
        botRight = CellAddresses.fromProto(proto.botRight)
        return RangeAddresses.from2Cells(topLeft, botRight)

    @staticmethod
    def from2Cells(firstCell: CellAddress, secondCell: CellAddress) -> RangeAddress:
        """accept any 2 cells, regardless of order, then construct a RangeAddress from that"""
        topLeftCell = CellIndex(min(firstCell.colIndex, secondCell.colIndex),
                                min(firstCell.rowIndex, secondCell.rowIndex))
        botRightCell = CellIndex(max(firstCell.colIndex, secondCell.colIndex),
                                 max(firstCell.rowIndex, secondCell.rowIndex))
        return RangeAddressImp(topLeftCell, botRightCell)

    @staticmethod
    def fromColRow(minCol, maxCol, minRow, maxRow) -> RangeAddress:
        return RangeAddresses.from2Cells(
            firstCell = CellAddresses.fromColRow(minCol,minRow),
            secondCell = CellAddresses.fromColRow(maxCol,maxRow)
        )

    @staticmethod
    def fromLabel(label: str) -> RangeAddress:
        isNormalRange = RangeAddresses.checkRangeAddressFormat(label)
        if isNormalRange.isOk():
            bareLabel = label
            cellLabels = bareLabel.split(":")
            cellAddresses = list(map(lambda cLabel: CellAddresses.fromLabel("" + cLabel), cellLabels))
            firstCell = cellAddresses[0]
            lastCell = cellAddresses[1]

            firstCol = min(firstCell.colIndex,lastCell.colIndex)
            firstRow = min(firstCell.rowIndex,lastCell.rowIndex)
            lastCol = max(firstCell.colIndex,lastCell.colIndex)
            lastRow = max(firstCell.rowIndex, lastCell.rowIndex)

            return RangeAddressImp(
                topLeft =CellIndex(firstCol, firstRow),
                botRight =CellIndex(lastCol, lastRow)
            )
        else:
            isWholeRange = RangeAddresses.checkWholeAddressFormat(label)
            if isWholeRange.isOk():
                bareLabel = label
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
                        topLeft =CellIndex(min(firstColIndex, secondColIndex), 1),
                        botRight =CellIndex(max(firstColIndex, secondColIndex), R.WorksheetConsts.rowLimit)
                    )
                elif firstPartIsRow and secondPartIsRow:
                    firstRowIndex = int(firstPart)
                    secondRowIndex = int(secondPart)
                    return RangeAddressImp(
                        topLeft =CellIndex(1, min(firstRowIndex, secondRowIndex)),
                        botRight =CellIndex(R.WorksheetConsts.colLimit, max(firstRowIndex, secondRowIndex))
                    )
                else:
                    raise ValueError("input label \"{lb}\" is not a valid whole column/row address")
            else:
                raise ValueError("input label \"{lb}\" is neither a normal range nor a whole range".format(lb=label))

    __rangeAddressPattern = re.compile("[a-zA-Z]+[1-9][0-9]*:[a-zA-Z]+[1-9][0-9]*")
    __wholeRangeAddressPattern = re.compile("([a-zA-Z]+|[1-9][0-9]*):([a-zA-Z]+|[1-9][0-9]*)")
    __singleWholeColAddressPattern = re.compile("[a-zA-Z]+")
    __singleWholeRowAddressPattern = re.compile("[1-9][0-9]*")

    @staticmethod
    def checkWholeAddressFormat(label:str)->Result[None,ErrorReport]:
        """
        :return true if a range address label is a whole col or whole row, false otherwise
        """
        return RangeAddresses.__checkAddressFormatAgainstPattern(label,RangeAddresses.__wholeRangeAddressPattern)

    @staticmethod
    def checkRangeAddressFormat(label: str) -> Result[None,ErrorReport]:
        """
        :param label: must be like "[a-zA-Z][1-9][0-9]*:[a-zA-Z][1-9][0-9]*" eg: "A1:B10"
        :return: Ok if address is legal, Err with an exception otherwise
        """
        return RangeAddresses.__checkAddressFormatAgainstPattern(label,RangeAddresses.__rangeAddressPattern)

    @staticmethod
    def __checkAddressFormatAgainstPattern(label: str, pattern) -> Result[None,ErrorReport]:
        """
        :param label: must be like "[a-zA-Z][1-9][0-9]*:[a-zA-Z][1-9][0-9]*" eg: "A1:B10"
        :return: Ok if address is legal, Err with an exception otherwise
        """
        if not isinstance(label, str):
            return Err(ValueError("range label must be a string."))
        else:
            matchResult = pattern.fullmatch(label)
            if matchResult is not None:
                return Ok(None)
            else:
                return Err(
                    ValueError("Range label \"{cdr}\" does not match the required pattern: {pt}"
                               .format(cdr=label, pt=str(pattern.pattern))))

    @staticmethod
    def parse(rangeAddress: Union[str, RangeAddress, Tuple[CellAddress, CellAddress]])->RangeAddress:
        parsedAddress = rangeAddress
        if isinstance(rangeAddress, str):
            parsedAddress = RangeAddresses.fromLabel(rangeAddress)

        if isinstance(rangeAddress, Tuple):
            ad1 = rangeAddress[0]
            ad2 = rangeAddress[1]
            parsedAddress = RangeAddressImp(ad1, ad2)
        return parsedAddress