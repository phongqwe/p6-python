from abc import ABC

from bicp_document_structure.column.Column import Column
from bicp_document_structure.column.ColumnContainer import ColumnContainer


class MutableColumnContainer(ColumnContainer,ABC):
    def setCol(self, col: Column):
        raise NotImplementedError()

    def removeCol(self, index: int):
        raise NotImplementedError()
