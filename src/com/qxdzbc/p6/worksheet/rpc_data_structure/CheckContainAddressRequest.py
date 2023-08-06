from dataclasses import dataclass

from com.qxdzbc.p6.cell.address.CellAddress import CellAddress
from com.qxdzbc.p6.util.ToProto import ToProto
from com.qxdzbc.p6.worksheet.rpc_data_structure.WorksheetId import WorksheetId
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

