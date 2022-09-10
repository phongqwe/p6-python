from dataclasses import dataclass
from typing import Optional

from com.qxdzbc.p6.document_structure.util.ToProto import ToProto
from com.qxdzbc.p6.document_structure.workbook.key.WorkbookKey import WorkbookKey
from com.qxdzbc.p6.document_structure.workbook.key.WorkbookKeys import WorkbookKeys
from com.qxdzbc.p6.proto.WorkbookProtos_pb2 import CreateNewWorksheetRequestProto

@dataclass
class CreateNewWorksheetRequest(ToProto[CreateNewWorksheetRequestProto]):
    wbKey:WorkbookKey
    newWorksheetName:Optional[str] = None

    @staticmethod
    def fromProto(proto: CreateNewWorksheetRequestProto):
        return CreateNewWorksheetRequest(
            wbKey = WorkbookKeys.fromProto(proto.wbKey),
            newWorksheetName = proto.newWorksheetName
        )

    def toProtoObj(self) -> CreateNewWorksheetRequestProto:
        rt = CreateNewWorksheetRequestProto()
        if self.newWorksheetName:
            rt.newWorksheetName = self.newWorksheetName
        rt.wbKey.CopyFrom(self.wbKey.toProtoObj())
        return rt
