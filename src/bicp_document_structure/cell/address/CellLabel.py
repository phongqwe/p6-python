from bicp_document_structure.cell.address.CellAddress import CellAddress
from bicp_document_structure.cell.address.CellIndex import CellIndex
from bicp_document_structure.util.AlphabetBaseNumberSystem import AlphabetBaseNumberSystem
from bicp_document_structure.util.Util import typeCheck


class CellLabel(CellAddress):
    def __init__(self,label:str):
        self.__label = label
        self.__indexAddress = CellLabel.__addressFromLabel(label)

    @staticmethod
    def __addressFromLabel(address: str) -> CellIndex:
        typeCheck(address, "address", str)
        col = ""
        row = ""
        for c in address:
            if c.isnumeric():
                row += c
            else:
                col += c

        colIndex = AlphabetBaseNumberSystem.translate(col)
        rowIndex = int(row)
        return CellIndex(colIndex, rowIndex)

    @property
    def rowIndex(self) -> int:
        return self.__indexAddress.rowIndex

    @property
    def colIndex(self) -> int:
        return self.__indexAddress.colIndex

    def __eq__(self, o) -> bool:
        return self.__indexAddress.__eq__(o)

    def __str__(self):
        return self.__label