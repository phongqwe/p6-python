import unittest
from dataclasses import dataclass
from typing import Optional

from com.emeraldblast.p6.document_structure.util.ToProto import ToProto, P
from com.emeraldblast.p6.document_structure.workbook.key.WorkbookKey import WorkbookKey
from com.emeraldblast.p6.proto.service.workbook.CreateNewWorksheetRequestProto_pb2 import CreateNewWorksheetRequestProto

@dataclass
class CreateNewWorksheetRequest(ToProto[CreateNewWorksheetRequestProto]):
    wbKey:WorkbookKey
    newWorksheetName:Optional[str] = None

    def toProtoObj(self) -> CreateNewWorksheetRequestProto:
        return CreateNewWorksheetRequestProto(
            wbKey = self.wbKey.toProtoObj(),
            newWorksheetName = self.newWorksheetName
        )


