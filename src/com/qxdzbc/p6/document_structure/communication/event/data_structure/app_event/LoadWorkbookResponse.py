from dataclasses import dataclass
from typing import Optional

from com.qxdzbc.p6.document_structure.communication.event.P6EventTable import P6EventTable
from com.qxdzbc.p6.document_structure.communication.event.data_structure.ToEventData import ToEventData
from com.qxdzbc.p6.document_structure.communication.notifier.eventData.EventData import EventData
from com.qxdzbc.p6.document_structure.util.ToProto import ToProto
from com.qxdzbc.p6.document_structure.util.report.error.ErrorReport import ErrorReport
from com.qxdzbc.p6.document_structure.workbook.WorkBook import Workbook
from com.qxdzbc.p6.proto.AppEventProtos_pb2 import LoadWorkbookResponseProto


# if TYPE_CHECKING:

#
@dataclass
class LoadWorkbookResponse(ToEventData,ToProto[LoadWorkbookResponseProto] ):
    def __init__(self, isError: bool, windowId: Optional[str], errorReport: Optional[ErrorReport] = None,
                 workbook: Optional[Workbook] = None):
        super().__init__()
        self.windowId = windowId
        self.workbook = workbook
        self.errorReport = errorReport
        self.isError = isError

    def toProtoObj(self) -> LoadWorkbookResponseProto:
        proto = LoadWorkbookResponseProto(isError = self.isError, windowId = self.windowId)
        if self.workbook:
            proto.workbook.CopyFrom(self.workbook.toProtoObj())
        if self.errorReport:
            proto.errorReport.CopyFrom(self.errorReport.toProtoObj())
        return proto