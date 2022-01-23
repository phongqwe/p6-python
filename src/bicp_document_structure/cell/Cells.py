from bicp_document_structure.cell.Cell import Cell
from bicp_document_structure.cell.CellJson import CellJson
from bicp_document_structure.cell.DataCell import DataCell
from bicp_document_structure.cell.address.CellAddresses import CellAddresses


class Cells:
    @staticmethod
    def cellFromJson(cellJson:CellJson)->Cell:
        cell = DataCell(
            address=CellAddresses.addressFromJson(cellJson.addr),
            value=cellJson.value,
            formula=None,
            script=cellJson.script,
        )
        return cell