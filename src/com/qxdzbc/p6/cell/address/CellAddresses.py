import re
from typing import Union, Tuple

from com.qxdzbc.p6.cell.address.CellAddress import CellAddress
from com.qxdzbc.p6.cell.address.CellIndex import CellIndex
from com.qxdzbc.p6.util.AlphabetBaseNumberSystem import AlphabetBaseNumberSystem
from com.qxdzbc.p6.util.report.error.ErrorReport import ErrorReport
from com.qxdzbc.p6.util.result.Err import Err
from com.qxdzbc.p6.util.result.Ok import Ok
from com.qxdzbc.p6.util.result.Result import Result
from com.qxdzbc.p6.proto.DocProtos_pb2 import CellAddressProto


class CellAddresses:
    __labelPattern = re.compile("[A-Za-z]+[1-9][0-9]*")




    @staticmethod
    def fromProto(proto: CellAddressProto):
        return CellIndex(proto.col, proto.row)

    @staticmethod
    def parse(address: CellAddress | Tuple[int, int] | str) -> CellAddress:
        if isinstance(address, CellAddress):
            return address
        if isinstance(address, Tuple):
            return CellAddresses.fromColRow(address[0], address[1])
        if isinstance(address, str):
            return CellAddresses.fromLabel(address)

    @staticmethod
    def fromLabel(address: str) -> CellAddress:
        """
        :param address: can be in form "<cell_address>" such as "A1"
        :return:
        """
        checkResult = CellAddresses.__checkCellAddressFormat(address)
        if checkResult.isOk():
            bareAddress = address
            col = ""
            row = ""
            for c in bareAddress:
                if c.isnumeric():
                    row += c
                else:
                    col += c
            colIndex = AlphabetBaseNumberSystem.toDecimal(col)
            rowIndex = int(row)
            return CellIndex(colIndex, rowIndex)
        else:
            raise checkResult.err

    @staticmethod
    def zero() -> CellAddress:
        """A special, invalid cell address"""
        return CellIndex(0, 0)

    @staticmethod
    def fromRowCol(row: int, col: int) -> CellAddress:
        """A special, invalid cell address"""
        return CellIndex(col, row)

    @staticmethod
    def fromColRow(col: int, row: int) -> CellAddress:
        """A special, invalid cell address"""
        return CellIndex(col, row)

    A1 = fromColRow(1,1)

    @staticmethod
    def __checkCellAddressFormat(address: str) -> Result[None, ErrorReport]:
        """
        check address format
        :param address: must be like "[A-Za-z]+[1-9][0-9]*" eg: "A1", "ABC123"
        :return: Ok if address is legal, Err with an exception otherwise
        """
        if not isinstance(address, str):
            return Err(ValueError("cell address must be a string."))
        else:
            matchResult = CellAddresses.__labelPattern.fullmatch(address)
            if matchResult is not None:
                return Ok(None)
            else:
                return Err(
                    ValueError(
                        "Cell address \"{cdr}\" does not match the required pattern: {pt}"
                            .format(cdr = address,
                                    pt = str(CellAddresses.__labelPattern.pattern))))
