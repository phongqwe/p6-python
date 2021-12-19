from bicp_document_structure.cell_container.MutableCellContainer import MutableCellContainer
from bicp_document_structure.column.ColumnContainer import MutableColumnContainer


class Worksheet(MutableCellContainer, MutableColumnContainer):
    @property
    def name(self)->str:
        raise NotImplementedError()