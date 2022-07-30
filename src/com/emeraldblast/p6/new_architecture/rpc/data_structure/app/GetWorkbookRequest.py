from dataclasses import dataclass
from typing import Optional

from com.emeraldblast.p6.document_structure.util.ToProto import ToProto, P
from com.emeraldblast.p6.document_structure.workbook.key.WorkbookKey import WorkbookKey
from com.emeraldblast.p6.proto.rpc.app.GetWorkbookRequestProto_pb2 import GetWorkbookRequestProto


@dataclass
class GetWorkbookRequest(ToProto[GetWorkbookRequestProto]):
    wbKey: Optional[WorkbookKey] = None
    wbName: Optional[str] = None
    wbIndex: Optional[int] = None

    def toProtoObj(self) -> GetWorkbookRequestProto:
        wbk = None
        name = None
        index = None
        if self.wbKey:
            wbk = self.wbKey.toProtoObj()
        if self.wbName:
            name = self.wbName
        if self.wbIndex is not None:
            index = self.wbIndex
        return GetWorkbookRequestProto(
            wbKey = wbk,
            wbName = name,
            wbIndex = index,
        )