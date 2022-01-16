import re

from bicp_document_structure.cell.address.CellIndex import CellIndex
from bicp_document_structure.util.AlphabetBaseNumberSystem import AlphabetBaseNumberSystem
from bicp_document_structure.util.result.Err import Err
from bicp_document_structure.util.result.Ok import Ok
from bicp_document_structure.util.result.Result import Result


class CellAddresses:
    __labelPattern = re.compile("@[A-Za-z]+[1-9][0-9]*")

    @staticmethod
    def addressFromLabel(address: str) -> CellIndex:
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
    def __checkCellAddressFormat(address: str) -> Result:
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
                                .format(cdr=address,
                                        pt=str(CellAddresses.__labelPattern.pattern))))
            else:
                return Err(ValueError("Cell address must start with \"@\""))