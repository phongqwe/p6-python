from typing import TypeVar, Generic

from com.emeraldblast.p6.document_structure.communication.event.P6Event import P6Event
from com.emeraldblast.p6.document_structure.util.ToJson import ToJson
from com.emeraldblast.p6.document_structure.util.ToProto import ToProto
from com.emeraldblast.p6.document_structure.workbook.WorkBook import Workbook

D = TypeVar("D")


class WorkbookEventData(ToJson, Generic[D]):

    def __init__(self, workbook: Workbook = None, event: P6Event = None, data: ToProto | D = None):
        self.workbook: Workbook = workbook
        self.event: P6Event = event
        self.data: ToProto = data


    def toJsonDict(self) -> dict:
        return {
            "workbook": self.workbook.name,
        }
