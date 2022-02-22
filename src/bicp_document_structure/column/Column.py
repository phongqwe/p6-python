from abc import ABC

from bicp_document_structure.column.ColumnJson import ColumnJson
from bicp_document_structure.range.Range import Range


class Column(Range, ABC):

    def range(self, firstRow: int, lastRow: int) -> Range:
        """create a range from this column"""
        raise NotImplementedError()

    # @property
    # def _onCellMutationEventHandler(self)->Callable[[Cell,P6Event],None]:
    #     raise NotImplementedError()

    @property
    def index(self) -> int:
        """index of this column"""
        raise NotImplementedError()

    def toJson(self)->ColumnJson:
        """create a json facade of this column"""
        raise NotImplementedError()