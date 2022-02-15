from typing import Union

from bicp_document_structure.cell.Cell import Cell
from bicp_document_structure.cell.CellJson import CellJson
from bicp_document_structure.cell.DataCell import DataCell
from bicp_document_structure.cell.address.CellIndex import CellIndex


class Cells:
    @staticmethod
    def cellFromJson(cellJson:Union[CellJson,str])->Cell:
        if isinstance(cellJson,str):
            cellJson = CellJson.fromJsonStr(cellJson)

        cell = DataCell(
            address=CellIndex(cellJson.address.col, cellJson.address.row),
            value=cellJson.value,
            formula=cellJson.formula,
            script=cellJson.script,
        )
        return cell