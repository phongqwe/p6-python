from dataclasses import dataclass
from typing import Optional

from com.qxdzbc.p6.cell.address.CellAddress import CellAddress
from com.qxdzbc.p6.cell.address.CellAddresses import CellAddresses
from com.qxdzbc.p6.cell.rpc_data_structure.CellId import CellId
from com.qxdzbc.p6.proto.DocProtos_pb2 import CellValueProto, CellContentProto
from com.qxdzbc.p6.util.CanCheckEmpty import CanCheckEmpty
from com.qxdzbc.p6.util.ToProto import ToProto
from com.qxdzbc.p6.workbook.key.WorkbookKey import WorkbookKey
from com.qxdzbc.p6.workbook.key.WorkbookKeys import WorkbookKeys
from com.qxdzbc.p6.rpc.data_structure.ToP6Msg import ToP6Msg
from com.qxdzbc.p6.proto.CellProtos_pb2 import CellUpdateRequestProto


@dataclass
class CellUpdateRequest(ToProto[CellUpdateRequestProto]):
    cellId:ToProto[CellId]
    cellContent:ToProto[CellContentProto]

    # @staticmethod
    # def fromProto(proto:CellUpdateRequestProto)->'CellUpdateRequest':
    #     rt = CellUpdateRequest(
    #         workbookKey = WorkbookKeys.fromProto(proto.workbookKey),
    #         worksheetName = proto.worksheetName,
    #         cellAddress = CellAddresses.fromProto(proto.cellAddress),
    #         value = None,
    #         formula = None,
    #     )
    #     # if proto.HasField("value"):
    #     if proto.value is not None:
    #         rt.value = proto.value
    #     # if proto.HasField("formula"):
    #     if proto.formula is not None:
    #         rt.formula = proto.formula
    #     return rt
    #
    # @staticmethod
    # def fromProtoBytes(protoByes:bytes)->'CellUpdateRequest':
    #     proto = CellUpdateRequestProto()
    #     proto.ParseFromString(protoByes)
    #     return CellUpdateRequest.fromProto(proto)

    def toProtoObj(self) -> CellUpdateRequestProto:
        rt = CellUpdateRequestProto(
            cellId = self.cellId.toProtoObj(),
            cellContent = self.cellContent.toProtoObj()
        )
        return rt