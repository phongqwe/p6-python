from abc import ABC

from bicp_document_structure.column.Column import Column


class ColumnContainer(ABC):
    def hasColumn(self, colIndex: int) -> bool:
        """check if this holder has a column at an index"""
        raise NotImplementedError()

    def getCol(self, colIndex: int) -> Column:
        """get column at an index"""
        raise NotImplementedError()
