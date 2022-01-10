from bicp_document_structure.app.result_aggregator.CompResultJson import CompResultJson
from bicp_document_structure.cell.CellJson import CellJson


class CompResult:
    def addCell(self,cell:CellJson):
        raise NotImplementedError()

    def clearCell(self):
        raise NotImplementedError()

    def toJson(self)->CompResultJson:
        raise NotImplementedError()