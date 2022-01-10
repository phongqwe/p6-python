from abc import ABC

from bicp_document_structure.app.run_result.RunResultJson import RunResultJson
from bicp_document_structure.cell.CellJson import CellJson


class RunResult(ABC):
    """ contains result after each run. A "run" happens when a request from the front end is received and execute successfully """
    def addCell(self,cell:CellJson):
        raise NotImplementedError()

    def clearCell(self):
        raise NotImplementedError()

    def toJson(self)->RunResultJson:
        raise NotImplementedError()