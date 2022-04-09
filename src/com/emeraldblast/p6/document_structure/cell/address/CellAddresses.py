import re
from typing import Union

from com.emeraldblast.p6.document_structure.cell.address.CellAddress import CellAddress
from com.emeraldblast.p6.document_structure.cell.address.CellAddressJson import CellAddressJson
from com.emeraldblast.p6.document_structure.cell.address.CellIndex import CellIndex
from com.emeraldblast.p6.document_structure.util.AlphabetBaseNumberSystem import AlphabetBaseNumberSystem
from com.emeraldblast.p6.document_structure.util.report.error.ErrorReport import ErrorReport
from com.emeraldblast.p6.document_structure.util.result.Err import Err
from com.emeraldblast.p6.document_structure.util.result.Ok import Ok
from com.emeraldblast.p6.document_structure.util.result.Result import Result
from com.emeraldblast.p6.proto.DocProtos_pb2 import CellAddressProto


class CellAddresses:
    __labelPattern = re.compile("@[A-Za-z]+[1-9][0-9]*")


    @staticmethod
    def fromProto(proto:CellAddressProto):
        return CellIndex(proto.col, proto.row)

    @staticmethod
    def addressFromJson(json: Union[CellAddressJson, str]) -> CellAddress:
        return CellIndex(json.col, json.row)

    @staticmethod
    def addressFromLabel(address: str) -> CellAddress:
        """
        :param address: can be in form "@<cell_address>" such as "@A1"
        :return:
        """
        checkResult = CellAddresses.__checkCellAddressFormat(address)
        if checkResult.isOk():
            bareAddress = address[1:]
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
    def fromRowCol(row:int,col:int) -> CellAddress:
        """A special, invalid cell address"""
        return CellIndex(col, row)

    @staticmethod
    def __checkCellAddressFormat(address: str) -> Result[None, ErrorReport]:
        """
        check address format
        :param address: must be like "@[A-Za-z]+[1-9][0-9]*" eg: "@A1", "@ABC123"
        :return: Ok if address is legal, Err with an exception otherwise
        """
        if not isinstance(address, str):
            return Err(ValueError("cell address must be a string."))
        else:
            if address.startswith("@"):
                matchResult = CellAddresses.__labelPattern.fullmatch(address)
                if matchResult is not None:
                    return Ok(None)
                else:
                    return Err(
                        ValueError(
                            "Cell address \"{cdr}\" does not match the required pattern: {pt}"
                                .format(cdr = address,
                                        pt = str(CellAddresses.__labelPattern.pattern))))
            else:
                return Err(ValueError("Cell address must start with \"@\""))