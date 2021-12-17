from com.github.xadkile.bicp.doc.data_structure.cell_container.MutableCellContainer import MutableCellContainer
from com.github.xadkile.bicp.doc.data_structure.range.Range import Range


class Column(Range, MutableCellContainer):

    def range(self, firstRow: int, lastRow: int) -> Range:
        """create a range from this colum"""
        pass

    @property
    def index(self) -> int:
        """index of this column"""
        pass