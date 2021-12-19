from abc import ABC

from bicp_document_structure.cell_container.MutableCellContainer import MutableCellContainer
from bicp_document_structure.column.MutableColumnContainer import MutableColumnContainer


class Worksheet(MutableCellContainer, MutableColumnContainer,ABC):
    @property
    def name(self)->str:
        raise NotImplementedError()