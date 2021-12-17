from com.github.xadkile.bicp.doc.data_structure.cell_container.MutableCellContainer import MutableCellContainer
from com.github.xadkile.bicp.doc.data_structure.column.ColumnContainer import MutableColumnContainer


class Worksheet(MutableCellContainer, MutableColumnContainer):
    @property
    def name(self)->str:
        pass