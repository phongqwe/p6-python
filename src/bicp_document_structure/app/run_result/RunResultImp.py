from typing import List

from bicp_document_structure.app.run_result.RunResult import RunResult
from bicp_document_structure.app.run_result.RunResultJson import RunResultJson
from bicp_document_structure.cell.Cell import Cell
from bicp_document_structure.cell.CellJson import CellJson


class RunResultImp(RunResult):

    def __init__(self, cellList:List[Cell]=None):
        if cellList is None:
            cellList = []
        self.__cellList = cellList

    def addCell(self,result:Cell):
        self.__cellList.append(result)

    def clearCell(self):
        self.__cellList = []

    def toJson(self) -> RunResultJson:
        cellJsons:List[CellJson] = list(map(lambda c: c.toJson, self.__cellList))
        return RunResultJson(cellJsons)


