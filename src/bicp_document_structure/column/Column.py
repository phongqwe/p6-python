from abc import ABC

from bicp_document_structure.cell_container.MutableCellContainer import MutableCellContainer
from bicp_document_structure.range.Range import Range


class Column(Range, MutableCellContainer, ABC):

    def range(self, firstRow: int, lastRow: int) -> Range:
        """create a range from this colum"""
        raise NotImplementedError()

    @property
    def index(self) -> int:
        """index of this column"""
        raise NotImplementedError()