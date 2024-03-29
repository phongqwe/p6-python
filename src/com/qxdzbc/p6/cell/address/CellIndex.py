from com.qxdzbc.p6.cell.address.CellAddress import CellAddress
from com.qxdzbc.p6.util.AlphabetBaseNumberSystem import AlphabetBaseNumberSystem
from com.qxdzbc.p6.proto.DocProtos_pb2 import CellAddressProto


class CellIndex(CellAddress):
    """ cell address in form of col index and row index """

    def addRow(self, i: int) -> 'CellAddress':
        return CellIndex(colIndex = self.colIndex,rowIndex = self.rowIndex+i)

    def addCol(self, i: int) -> 'CellAddress':
        return CellIndex(colIndex = self.colIndex+i, rowIndex = self.rowIndex)

    def __init__(self, colIndex: int, rowIndex: int):
        self.__rowIndex = rowIndex
        self.__colIndex = colIndex

    def toProtoObj(self) -> CellAddressProto:
        addr = CellAddressProto()
        addr.row = self.rowIndex
        addr.col = self.colIndex
        return addr

    @property
    def rowIndex(self) -> int:
        return self.__rowIndex

    @property
    def colIndex(self) -> int:
        return self.__colIndex

    def __str__(self):
        # return "C({col}:{row})".format(col = self.__colIndex, row = self.__rowIndex)
        return self.label

    @property
    def label(self) -> str:
        colLabel = AlphabetBaseNumberSystem.fromDecimal(self.colIndex)
        return "{cl}{rl}".format(cl = colLabel, rl = str(self.rowIndex))
