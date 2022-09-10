from dataclasses import dataclass

from com.qxdzbc.p6.document_structure.cell.address.CellAddress import CellAddress
from com.qxdzbc.p6.document_structure.util.ToProto import ToProto
from com.qxdzbc.p6.new_architecture.rpc.data_structure.worksheet.WorksheetId import WorksheetId
from com.qxdzbc.p6.proto.WorksheetProtos_pb2 import CheckContainAddressRequestProto


@dataclass
class CheckContainAddressRequest(ToProto[CheckContainAddressRequestProto]):
    wsId: WorksheetId
    cellAddress: CellAddress
    def toProtoObj(self) -> CheckContainAddressRequestProto:
        return CheckContainAddressRequestProto(
            wsId = self.wsId.toProtoObj(),
            cellAddress = self.cellAddress.toProtoObj()
        )

