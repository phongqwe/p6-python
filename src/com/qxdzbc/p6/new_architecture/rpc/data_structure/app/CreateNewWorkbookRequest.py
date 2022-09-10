from dataclasses import dataclass
from typing import Optional

from com.qxdzbc.p6.document_structure.util.ToProto import ToProto, P
from com.qxdzbc.p6.proto.AppProtos_pb2 import CreateNewWorkbookRequestProto


@dataclass
class CreateNewWorkbookRequest(ToProto[CreateNewWorkbookRequestProto]):
    windowId: Optional[str] = None
    workbookName:Optional[str] = None

    def toProtoObj(self) -> CreateNewWorkbookRequestProto:
        rt=CreateNewWorkbookRequestProto()
        if self.workbookName:
            rt.workbookName = self.workbookName
        if self.windowId:
            rt.windowId = self.windowId
        return rt

    @staticmethod
    def fromProtoBytes(data: bytes) -> 'CreateNewWorkbookRequest':
        proto = CreateNewWorkbookRequestProto()
        proto.ParseFromString(data)
        rt= CreateNewWorkbookRequest()
        if proto.HasField("windowId"):
            rt.windowId = proto.windowId
        if proto.HasField("workbookName"):
            rt.workbookName = proto.workbookName
        return rt

