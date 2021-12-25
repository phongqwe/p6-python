import re

from bicp_document_structure.cell.address.CellAddress import CellAddress
from bicp_document_structure.cell.address.CellIndex import CellIndex
from bicp_document_structure.util.AlphabetBaseNumberSystem import AlphabetBaseNumberSystem
from bicp_document_structure.util.result.Err import Err
from bicp_document_structure.util.result.Ok import Ok
from bicp_document_structure.util.result.Result import Result


class CellLabel(CellAddress):
    __labelPattern = re.compile("@[A-Za-z]+[1-9][0-9]*")

    def __init__(self, label: str):
        self.__label = label
        self.__indexAddress = CellLabel.__addressFromLabel(label)

    @staticmethod
    def __addressFromLabel(address: str) -> CellIndex:
        """
        :param address: can be in form "@<cell_address>" such as "@A1"
        :return:
        """
        checkResult = CellLabel.__checkCellAddressFormat(address)
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
                matchResult = CellLabel.__labelPattern.fullmatch(address)
                if matchResult is not None:
                    return Ok(None)
                else:
                    return Err(
                        ValueError(
                            "Cell address \"{cdr}\" does not match the required pattern: {pt}".format(cdr=address,
                                                                                                      pt=str(
                                                                                                          CellLabel.__labelPattern.pattern))))
            else:
                return Err(ValueError("Cell address must start with \"@\""))

    @property
    def rowIndex(self) -> int:
        return self.__indexAddress.rowIndex

    @property
    def colIndex(self) -> int:
        return self.__indexAddress.colIndex

    def __eq__(self, o) -> bool:
        return self.__indexAddress.__eq__(o)

    def __str__(self):
        return self.__label[1:]
