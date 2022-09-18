from abc import ABC

from com.qxdzbc.p6.util.ToProto import ToProto
from com.qxdzbc.p6.proto.DocProtos_pb2 import CellAddressProto


class CellAddress(ToProto[CellAddressProto], ABC):
    """
    an interface representing a position of a cell, including row and column index
    """

    def addRow(self,i:int)->'CellAddress':
        raise NotImplementedError()
    def addCol(self,i:int)->'CellAddress':
        raise NotImplementedError()

    def colDif(self, anotherCellAddress: 'CellAddress'):
        return self.colIndex - anotherCellAddress.colIndex

    def rowDif(self, anotherCellAddress: 'CellAddress'):
        return self.rowIndex - anotherCellAddress.rowIndex

    @property
    def rowIndex(self) -> int:
        """ read-only row index """
        raise NotImplementedError()

    @property
    def colIndex(self) -> int:
        """ read-only col index """
        raise NotImplementedError()

    def __eq__(self, o) -> bool:
        if isinstance(o, CellAddress):
            sameRow = (self.rowIndex == o.rowIndex)
            sameCol = (self.colIndex == o.colIndex)
            return sameRow and sameCol
        else:
            return False

    @property
    def label(self) -> str:
        """:return label of this cell address in correct format (eg: @A1), that can be used to refer to this address directly"""
        raise NotImplementedError()

    @property
    def rawLabel(self) -> str:
        """:return label of this cell address in raw format (eg: A1), that can NOT be used to refer to this address directly"""
        raise NotImplementedError()

    def __hash__(self) -> int:
        key = (self.colIndex, self.rowIndex)
        return hash(key)

    def toTuple(self) -> (int, int):
        """create a tuple of [col,row]"""
        return self.colIndex, self.rowIndex
