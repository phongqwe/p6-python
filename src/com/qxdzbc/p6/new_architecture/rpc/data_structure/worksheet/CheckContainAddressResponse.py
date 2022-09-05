from dataclasses import dataclass

from com.qxdzbc.p6.document_structure.util.ToProto import ToProto, P
from com.qxdzbc.p6.proto.rpc.worksheet.WorksheetServiceProtos_pb2 import CheckContainAddressResponseProto

@dataclass
class CheckContainAddressResponse(ToProto[CheckContainAddressResponseProto]):
    contain:bool
    
    def toProtoObj(self) -> CheckContainAddressResponseProto:
        return CheckContainAddressResponseProto(contain = self.contain)
    
    @staticmethod
    def fromProto(proto:CheckContainAddressResponseProto):
        return CheckContainAddressResponse(proto.contain)