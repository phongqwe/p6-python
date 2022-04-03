from typing import TypeVar, Generic

from com.emeraldblast.p6.document_structure.communication.event.P6Event import P6Event
from com.emeraldblast.p6.document_structure.util.ToJson import ToJson
from com.emeraldblast.p6.document_structure.util.ToProto import ToProto
from com.emeraldblast.p6.document_structure.workbook.WorkBook import Workbook

D = TypeVar("D")


class WorkbookEventData(ToJson, Generic[D]):

    def __init__(self, workbook: Workbook, event: P6Event, data: ToProto | D = None):
        self._workbook: Workbook = workbook
        self.event: P6Event = event
        self._data: ToProto = data

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
