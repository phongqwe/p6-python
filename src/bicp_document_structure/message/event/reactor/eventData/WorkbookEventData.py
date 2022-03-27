from typing import TypeVar, Generic

from bicp_document_structure.message.event.P6Event import P6Event
from bicp_document_structure.message.event.reactor.eventData.WithWorkbookData import WithWorkbookData
from bicp_document_structure.util.ToJson import ToJson
from bicp_document_structure.util.ToProto import ToProto
from bicp_document_structure.workbook.WorkBook import Workbook

D = TypeVar("D")


class WorkbookEventData(ToJson, WithWorkbookData, Generic[D]):

    def __init__(self, workbook: Workbook, event: P6Event, isError: bool = False, data: ToProto | D = None):
        self._workbook: Workbook = workbook
        self.event: P6Event = event
        self._data: ToProto = data
        self._isError: bool = isError

    @property
    def isError(self) -> bool:
        return self._isError

    @property
    def workbook(self):
        return self._workbook

    @property
    def data(self) -> ToProto:
        return self._data

    def toJsonDict(self) -> dict:
        return {
            "workbook": self.workbook.name,
        }
