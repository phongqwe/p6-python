from dataclasses import dataclass

from com.qxdzbc.p6.document_structure.util.ToProto import ToProto
from com.qxdzbc.p6.document_structure.workbook.key.WorkbookKey import WorkbookKey
from com.qxdzbc.p6.document_structure.workbook.key.WorkbookKeys import WorkbookKeys
from com.qxdzbc.p6.proto.rpc.workbook.WorkbooKServiceProtos_pb2 import RenameWorksheetRequestProto


@dataclass
class RenameWorksheetRequest(ToProto[RenameWorksheetRequestProto]):

    wbKey: WorkbookKey
    oldName: str
    newName: str

    def toProtoObj(self) -> RenameWorksheetRequestProto:
        return RenameWorksheetRequestProto(
            wbKey = self.wbKey.toProtoObj(),
            oldName = self.oldName,
            newName = self.newName,
        )


    @staticmethod
    def fromProto(proto:RenameWorksheetRequestProto)->'RenameWorksheetRequest':
        return RenameWorksheetRequest(
            newName = proto.newName,
            oldName = proto.oldName,
            wbKey = WorkbookKeys.fromProto(proto.workbookKey)
        )
    @staticmethod
    def fromProtoBytes(data:bytes)->'RenameWorksheetRequest':
        protoRequest = RenameWorksheetRequestProto()
        protoRequest.ParseFromString(data)
        return RenameWorksheetRequest.fromProto(protoRequest)