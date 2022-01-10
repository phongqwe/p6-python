from abc import ABC

from bicp_document_structure.cell.Cell import Cell


class CellWriter(ABC):
    @property
    def cell(self)->Cell:
        raise NotImplementedError()

    def writeText(self):
        raise NotImplementedError()

    def writeCode(self):
        raise NotImplementedError()