from typing import Union, Any, Callable

from com.emeraldblast.p6.document_structure.cell.address.CellAddresses import CellAddresses
from com.emeraldblast.p6.proto.DocProtos_pb2 import CellProto

from com.emeraldblast.p6.document_structure.cell.Cell import Cell
from com.emeraldblast.p6.document_structure.cell.CellJson import CellJson
from com.emeraldblast.p6.document_structure.cell.DataCell import DataCell
from com.emeraldblast.p6.document_structure.cell.EventCell import EventCell
from com.emeraldblast.p6.document_structure.cell.WriteBackCell import WriteBackCell
from com.emeraldblast.p6.document_structure.cell.address.CellAddress import CellAddress
from com.emeraldblast.p6.document_structure.cell.address.CellIndex import CellIndex
from com.emeraldblast.p6.document_structure.cell_container.MutableCellContainer import MutableCellContainer
from com.emeraldblast.p6.document_structure.communication.event.P6Event import P6Event


class Cells:
    """
    Cell factory
    """
    @staticmethod
    def fromProto(proto:CellProto)->Cell:
        v = proto.value
        try:
            vf = float(v)
            v = vf
        except Exception as e:
            pass

        rt = DataCell(
            address = CellAddresses.fromProto(proto.address),
            value = v,
            formula = proto.formula,
            script = proto.script,
        )
        return rt


    @staticmethod
    def cellFromJson(cellJson: Union[CellJson, str]) -> Cell:
        if isinstance(cellJson, str):
            cellJson = CellJson.fromJsonStr(cellJson)
        cell = DataCell(
            address = CellIndex(cellJson.address.col, cellJson.address.row),
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
