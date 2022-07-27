from dataclasses import dataclass
from typing import Optional

from com.emeraldblast.p6.document_structure.communication.event.data_structure.common.ErrorIndicator import \
    ErrorIndicator

from com.emeraldblast.p6.document_structure.util.ToProto import ToProto, P
from com.emeraldblast.p6.document_structure.util.report.error.ErrorReport import ErrorReport
from com.emeraldblast.p6.document_structure.workbook.key.WorkbookKey import WorkbookKey
from com.emeraldblast.p6.proto.service.workbook.SetWbName_pb2 import SetWbNameRequestProto, SetWbNameResponseProto


@dataclass
class SetWbNameRequest(ToProto[SetWbNameRequestProto]):
    wbKey:WorkbookKey
    newName:str
    def toProtoObj(self) -> SetWbNameRequestProto:
        return SetWbNameRequestProto(
            wbKey = self.wbKey.toProtoObj(),
            newName = self.newName
        )


@dataclass
class SetWbNameResponse(ToProto[SetWbNameResponseProto]):
    errorReport:Optional[ErrorReport] = None
    @staticmethod
    def fromProto(proto:SetWbNameResponseProto):
        err = None
        if proto.HasField("errorReport"):
            err = ErrorReport.fromProto(proto.errorReport)
        return SetWbNameResponse(
            errorReport = err
        )
    def toProtoObj(self)->SetWbNameResponseProto:
        proto = SetWbNameResponseProto()
        if self.errorReport is not None:
            proto.errorReport.CopyFrom(self.errorReport.toProtoObj())
        return proto
