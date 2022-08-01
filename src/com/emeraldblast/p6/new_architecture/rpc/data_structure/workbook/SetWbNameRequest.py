from dataclasses import dataclass
from typing import Optional

from com.emeraldblast.p6.document_structure.communication.event.data_structure.common.ErrorIndicator import \
    ErrorIndicator

from com.emeraldblast.p6.document_structure.util.ToProto import ToProto, P
from com.emeraldblast.p6.document_structure.util.report.error.ErrorReport import ErrorReport
from com.emeraldblast.p6.document_structure.workbook.key.WorkbookKey import WorkbookKey
from com.emeraldblast.p6.proto.rpc.workbook.WorkbooKServiceProtos_pb2 import SetWbKeyRequestProto


@dataclass
class SetWbNameRequest(ToProto[SetWbKeyRequestProto]):
    wbKey:WorkbookKey
    newWbKey:WorkbookKey
    def toProtoObj(self) -> SetWbKeyRequestProto:
        return SetWbKeyRequestProto(
            wbKey = self.wbKey.toProtoObj(),
            newWbKey = self.newWbKey.toProtoObj()
        )