from typing import Union, Any, Callable

from bicp_document_structure.cell.Cell import Cell
from bicp_document_structure.cell.CellJson import CellJson
from bicp_document_structure.cell.DataCell import DataCell
from bicp_document_structure.cell.EventCell import EventCell
from bicp_document_structure.cell.WriteBackCell import WriteBackCell
from bicp_document_structure.cell.address.CellAddress import CellAddress
from bicp_document_structure.cell.address.CellIndex import CellIndex
from bicp_document_structure.cell_container.MutableCellContainer import MutableCellContainer
from bicp_document_structure.message.event.P6Event import P6Event
from bicp_document_structure.formula_translator.FormulaTranslator import FormulaTranslator


class Cells:
    """
    Cell factory
    """

    @staticmethod
    def cellFromJson(cellJson: Union[CellJson, str],translatorGetter:Callable[[],FormulaTranslator]|None= None) -> Cell:
        if isinstance(cellJson, str):
            cellJson = CellJson.fromJsonStr(cellJson)

        cell = DataCell(
            address = CellIndex(cellJson.address.col, cellJson.address.row),
            translatorGetter = translatorGetter,
            value = cellJson.value,
            formula = cellJson.formula,
            script = cellJson.script,
        )
        return cell

    @staticmethod
    def data(address: CellAddress,
             value: Any = None,
             formula: str = None,
             script: str = None) -> DataCell:
        return DataCell(address, value, formula, script)

    @staticmethod
    def eventCell(innerCell: Cell,
                  onCellChange: Callable[[Cell, P6Event], None] = None) -> EventCell:
        return EventCell(innerCell, onCellChange)

    @staticmethod
    def writeBack(cell: Cell, container: MutableCellContainer) -> WriteBackCell:
        return WriteBackCell(cell, container)
