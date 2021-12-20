from abc import ABC

from bicp_document_structure.cell_container.MutableCellContainer import MutableCellContainer
from bicp_document_structure.column.MutableColumnContainer import MutableColumnContainer
from bicp_document_structure.worksheet.UserFriendlyWorksheet import UserFriendlyWorksheet


class Worksheet(MutableCellContainer, MutableColumnContainer, UserFriendlyWorksheet, ABC):
    @property
    def name(self) -> str:
        raise NotImplementedError()
