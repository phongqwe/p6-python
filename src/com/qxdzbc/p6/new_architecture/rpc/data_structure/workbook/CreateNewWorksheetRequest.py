import unittest
from dataclasses import dataclass
from typing import Optional

from com.qxdzbc.p6.document_structure.util.ToProto import ToProto, P
from com.qxdzbc.p6.document_structure.workbook.key.WorkbookKey import WorkbookKey
from com.qxdzbc.p6.proto.rpc.workbook.WorkbooKServiceProtos_pb2 import CreateNewWorksheetRequestProto


@dataclass
class CreateNewWorksheetRequest(ToProto[CreateNewWorksheetRequestProto]):
    wbKey:WorkbookKey
    newWorksheetName:Optional[str] = None

    def toProtoObj(self) -> CreateNewWorksheetRequestProto:
        return CreateNewWorksheetRequestProto(
            wbKey = self.wbKey.toProtoObj(),
            newWorksheetName = self.newWorksheetName
        )


