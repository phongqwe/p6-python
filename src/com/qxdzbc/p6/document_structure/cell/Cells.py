from typing import Union, Any, Callable

from com.qxdzbc.p6.document_structure.cell.Cell import Cell
from com.qxdzbc.p6.document_structure.cell.CellJson import CellJson
from com.qxdzbc.p6.document_structure.cell.DataCell import DataCell
from com.qxdzbc.p6.document_structure.cell.EventCell import EventCell
from com.qxdzbc.p6.document_structure.cell.WriteBackCell import WriteBackCell
from com.qxdzbc.p6.document_structure.cell.address.CellAddress import CellAddress
from com.qxdzbc.p6.document_structure.cell.address.CellAddresses import CellAddresses
from com.qxdzbc.p6.document_structure.cell.address.CellIndex import CellIndex
from com.qxdzbc.p6.document_structure.cell_container.MutableCellContainer import MutableCellContainer
from com.qxdzbc.p6.new_architecture.communication import P6Event
from com.qxdzbc.p6.proto.DocProtos_pb2 import CellProto


class Cells:
    """
    Cell factory
    """
    @staticmethod
    def fromProto(proto:CellProto)->Cell:
        vParsed = None
        isValue = not proto.HasField("formula")
        if proto.HasField("value") and isValue:
            v = proto.value
            vParsed = None
            if v.HasField("bool"):
                if v.bool == "True":
                    vParsed = True
                else:
                    vParsed = False
            if v.HasField("num"):
                vParsed = float(v.num)

        formula = None
        if proto.HasField("formula"):
            formula = proto.formula

        rt = DataCell(
            address = CellAddresses.fromProto(proto.address),
            value = vParsed,
            formula = formula,
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
