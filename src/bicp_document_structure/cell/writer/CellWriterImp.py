from collections import Callable

from bicp_document_structure.cell.Cell import Cell
from bicp_document_structure.cell.writer.CellWriter import CellWriter


class CellWriterImp(CellWriter):
    def __init__(self,
                 cell:Cell,
                 onUpdate:Callable[[Cell],None]):
        self.__cellAddress = cell.address
        self.__innerCell = cell
        self.__onUpdate = onUpdate

    @property
    def cell(self) -> Cell:
        return self.__innerCell

    def writeText(self):
        newCell = self.__innerCell
        pass

    def writeCode(self):
        pass

