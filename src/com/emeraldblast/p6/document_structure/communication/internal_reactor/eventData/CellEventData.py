from com.emeraldblast.p6.document_structure.cell.Cell import Cell
from com.emeraldblast.p6.document_structure.communication.event.P6Event import P6Event
from com.emeraldblast.p6.document_structure.util.ToJson import ToJson
from com.emeraldblast.p6.document_structure.util.ToProto import ToProto
from com.emeraldblast.p6.document_structure.workbook.WorkBook import Workbook
from com.emeraldblast.p6.document_structure.worksheet.Worksheet import Worksheet


class CellEventData(ToJson):

    def __init__(self,
                 workbook: Workbook = None,
                 worksheet: Worksheet = None,
                 cell: Cell = None,
                 event: P6Event = None,
                 isError: bool = False,
                 data: ToProto = None):
        self.cell = cell
        self.worksheet = worksheet
        self.workbook = workbook
        self.event: P6Event = event
        self.isError = isError
        self._data = data

    @property
    def data(self) -> ToProto | None:
        return self._data

    @data.setter
    def data(self, newData: ToProto):
        self._data = newData

    def toJsonDict(self) -> dict:
        path = self.workbook.workbookKey.filePath
        pathJson = None
        if path is not None:
            pathJson = str(path)
        return {
            "workbook": {
                "name": self.workbook.name,
                "path": pathJson
            },
            "worksheet": self.worksheet.name,
            "cell": self.cell.toJson().toJsonDict()
        }
