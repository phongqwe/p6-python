from typing import List

from bicp_document_structure.app.result_aggregator.CompResult import CompResult
from bicp_document_structure.app.result_aggregator.CompResultJson import CompResultJson
from bicp_document_structure.cell.Cell import Cell
from bicp_document_structure.cell.CellJson import CellJson


class CompResultImp(CompResult):

    def __init__(self, cellList:List[Cell]=None):
        if cellList is None:
            cellList = []
        self.__cellList = cellList

    def addCell(self,result:Cell):
        self.__cellList.append(result)

    def clearCell(self):
        self.__cellList = []

    def toJson(self) -> CompResultJson:
        cellJsons:List[CellJson] = list(map(lambda c: c.toJson, self.__cellList))
        return CompResultJson(cellJsons)


