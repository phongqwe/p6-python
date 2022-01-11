from abc import ABC

from bicp_document_structure.app.run_result.RunResultJson import RunResultJson
from bicp_document_structure.cell.address.CellAddress import CellAddress
from bicp_document_structure.workbook.WorkbookKey import WorkbookKey


class RunResult(ABC):
    """ contains result after each run. A "run" happens when a request from the front end is received and execute successfully """

    def addMutatedCell(self, workbookKey: WorkbookKey, worksheetName: str, cell: CellAddress):
        """ add a mutated Cell to this RunResult """
        raise NotImplementedError()

    def addDeletedCell(self, workbookKey: WorkbookKey, worksheetName: str, cell: CellAddress):
        """add address of cells that have been deleted"""
        raise NotImplementedError()

    def clearResult(self):
        """ remove everything from this RunResult object """
        raise NotImplementedError()

    def toJson(self) -> RunResultJson:
        raise NotImplementedError()
