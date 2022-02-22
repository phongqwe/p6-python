from bicp_document_structure.common.ToJsonStr import ToJson
from bicp_document_structure.workbook.WorkBook import Workbook


class WorkbookEventData(ToJson):

    def __init__(self, workbook: Workbook):
        self.workbook = workbook


    def toJsonDict(self) -> dict:
        return {
            "workbook": self.workbook.name,
        }
