from bicp_document_structure.cell.Cell import Cell
from bicp_document_structure.message.event.P6Event import P6Event
from bicp_document_structure.message.event.reactor.eventData.WithWorkbookData import WithWorkbookData
from bicp_document_structure.util.ToJson import ToJson
from bicp_document_structure.workbook.WorkBook import Workbook
from bicp_document_structure.worksheet.Worksheet import Worksheet


class CellEventData(ToJson,WithWorkbookData):

    def __init__(self, workbook: Workbook, worksheet: Worksheet, cell: Cell,event:P6Event):
        self.cell = cell
        self.worksheet = worksheet
        self._workbook = workbook
        self.event:P6Event = event

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

    @property
    def workbook(self):
        return self._workbook

