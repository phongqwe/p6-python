from typing import List

from bicp_document_structure.app.run_result.RunResult import RunResult
from bicp_document_structure.app.run_result.RunResultJson import RunResultJson
from bicp_document_structure.cell.Cell import Cell
from bicp_document_structure.cell.address.CellAddress import CellAddress


class RunResultImp(RunResult):

    def __init__(self, mutatedCellList:List[Cell]=None, deletedCells:List[CellAddress]=None):
        if mutatedCellList is None:
            mutatedCellList = []
        if deletedCells is None:
            deletedCells = []
        self.__mutatedCellList = mutatedCellList
        self.__deletedCellList = deletedCells

    def addMutatedCell(self,result:Cell):
        self.__mutatedCellList.append(result)

    def addDeletedCell(self, cellAddress: CellAddress):
        self.__deletedCellList.append(cellAddress)

    def clearResult(self):
        self.__mutatedCellList = []
        self.__deletedCellList = []

    def toJson(self) -> RunResultJson:
        mutatedCellJson = []
        for cell in self.__mutatedCellList:
            mutatedCellJson.append(cell.toJson())

        # cellJsons:List[CellJson] = list(map(lambda c: c.toJson(), self.__mutatedCellList))
        return RunResultJson(mutatedCellJson)


