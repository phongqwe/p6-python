from abc import ABC

from com.emeraldblast.p6.document_structure.app.run_result.RunResultJson import RunResultJson
from com.emeraldblast.p6.document_structure.app.workbook_container.WorkbookContainer import WorkbookContainer
from com.emeraldblast.p6.document_structure.cell.address.CellAddress import CellAddress
from com.emeraldblast.p6.document_structure.workbook.key.WorkbookKey import WorkbookKey


class RunResult(ABC):
    
    def removeDeletedCell(self,workbookKey: WorkbookKey, worksheetName: str, cellAddress: CellAddress):
        """ remove a deleted cell from this result"""
        raise NotImplementedError()

    def removeMutatedCell(self,workbookKey: WorkbookKey, worksheetName: str, cellAddress: CellAddress):
        """remove a deleted cell from this result"""
        raise NotImplementedError()

    def addMutatedCell(self, workbookKey: WorkbookKey, worksheetName: str, cellAddress: CellAddress):
        """ add a mutated Cell to this RunResult """
        raise NotImplementedError()

    def addDeletedCell(self, workbookKey: WorkbookKey, worksheetName: str, cellAddress: CellAddress):
        """add address of cells that have been deleted"""
        raise NotImplementedError()

    def containCellInDeleted(self,workbookKey: WorkbookKey, worksheetName: str, cellAddress: CellAddress):
        """ check if this RunResult has a CellAddress as a deleted cell """
        raise NotImplementedError()

    def containCellInMutated(self,workbookKey: WorkbookKey, worksheetName: str, cellAddress: CellAddress):
        """ check if this RunResult has a CellAddress as a mutated cell """
        raise NotImplementedError()

    def clearResult(self):
        """ remove everything from this RunResult object """
        raise NotImplementedError()

    def toJson(self,workbookContainer:WorkbookContainer) -> RunResultJson:
        """
        :param workbookContainer: for looking up cell data
        """
        raise NotImplementedError()
