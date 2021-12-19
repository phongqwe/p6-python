from abc import ABC

from bicp_document_structure.cell.address.CellAddress import CellAddress


class RangeAddress(ABC):
    @property
    def firstAddress(self) -> CellAddress:
        raise NotImplementedError()

    @property
    def lastAddress(self) -> CellAddress:
        raise NotImplementedError()

    def rowCount(self) -> int:
        raise NotImplementedError()

    def colCount(self) -> int:
        raise NotImplementedError()


