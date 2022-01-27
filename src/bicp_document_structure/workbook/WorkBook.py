from abc import ABC
from typing import Optional, Union, List

from bicp_document_structure.report.error.ErrorReport import ErrorReport
from bicp_document_structure.report.error.ErrorReports import ErrorReports
from bicp_document_structure.util.result.Result import Result
from bicp_document_structure.workbook.WorkbookJson import WorkbookJson
from bicp_document_structure.workbook.WorkbookKey import WorkbookKey
from bicp_document_structure.worksheet.Worksheet import Worksheet


class Workbook(ABC):

    def reRun(self):
        """rerun all worksheet in this workbook"""
        for sheet in self.sheets:
            sheet.reRun()

    @property
    def sheets(self) -> List[Worksheet]:
        """return a list of all sheet in this workbook"""
        raise NotImplementedError()

    @property
    def workbookKey(self) -> WorkbookKey:
        raise NotImplementedError()

    @workbookKey.setter
    def workbookKey(self, newKey: WorkbookKey):
        raise NotImplementedError()

    @property
    def activeSheet(self) -> Optional[Worksheet]:
        raise NotImplementedError()

    def setActiveSheet(self, indexOrName: Union[int, str]):
        raise NotImplementedError()

    def getSheetByName(self, name: str) -> Optional[Worksheet]:
        """
        :param name: sheet name
        :return: the sheet having that name or None if no such sheet exists
        """
        raise NotImplementedError()

    def getSheetByIndex(self, index: int) -> Optional[Worksheet]:
        """
        :param index: index of a sheet
        :return: the sheet at that index, or None if no such sheet exists
        """
        raise NotImplementedError()

    def getSheet(self, nameOrIndex: Union[str, int]) -> Optional[Worksheet]:
        """
        get a sheet either by name or index
        :param nameOrIndex: name or index
        :return: the sheet at that index/name, or None if no such sheet exists
        """
        raise NotImplementedError()

    def isEmpty(self) -> bool:
        """
        :return: true if this workbook contains zero sheet
        """
        raise NotImplementedError()

    @property
    def sheetCount(self) -> int:
        raise NotImplementedError()

    @property
    def name(self) -> str:
        raise NotImplementedError()

    @name.setter
    def name(self, newName: str):
        raise NotImplementedError()

    def createNewSheet(self, newSheetName: Optional[str]) -> Worksheet:
        """
        add a new empty sheet to this workbook
        :param newSheetName: name of the new sheet
        :return the new worksheet
        :raise ValueError if the newSheetName already exists
        """
        createRs = self.createNewSheetRs(newSheetName)
        if createRs.isOk():
            return createRs.value
        else:
            raise ErrorReports.toException(createRs.err)

    def createNewSheetRs(self, newSheetName: Optional[str]) -> Result[Worksheet,ErrorReport]:
        """
        add a new empty sheet to this workbook
        :param newSheetName: name of the new sheet
        :return Result object containing the new worksheet or ErrorRepor
        """
        raise NotImplementedError()

    def removeSheetByName(self, sheetName: str) -> Optional[Worksheet]:
        """ remove sheet by name. If the target sheet does not exist, simply return"""
        removeRs = self.removeSheetByNameRs(sheetName)
        if removeRs.isOk():
            return removeRs.value
        else:
            raise ErrorReports.toException(removeRs.err)

    def removeSheetByIndex(self, index: int) -> Optional[Worksheet]:
        """ remove sheet by index. If the target sheet does not exist, simply return"""
        removeRs = self.removeSheetByIndexRs(index)
        if removeRs.isOk():
            return removeRs.value
        else:
            raise ErrorReports.toException(removeRs.err)

    def removeSheet(self, nameOrIndex: Union[str, int]) -> Optional[Worksheet]:
        """ remove sheet by either index or name. If the target sheet does not exist, simply return"""
        removeRs = self.removeSheetRs(nameOrIndex)
        if removeRs.isOk():
            return removeRs.value
        else:
            raise ErrorReports.toException(removeRs.err)

    def removeSheetByNameRs(self, sheetName: str) -> Result[Worksheet,ErrorReport]:
        """ remove sheet by name. If the target sheet does not exist, simply return"""
        raise NotImplementedError()

    def removeSheetByIndexRs(self, index: int) -> Result[Worksheet,ErrorReport]:
        """ remove sheet by index. If the target sheet does not exist, simply return"""
        raise NotImplementedError()

    def removeSheetRs(self, nameOrIndex: Union[str, int]) -> Result[Worksheet,ErrorReport]:
        """ remove sheet by either index or name. If the target sheet does not exist, simply return"""
        raise NotImplementedError()

    def toJson(self) -> WorkbookJson:
        jsons = []
        for sheet in self.sheets:
            jsons.append(sheet.toJson())
        return WorkbookJson(self.name, jsons)

    def listWorksheet(self) -> str:
        """return a list of sheet as string"""
        rt = ""
        for (i, sheet) in enumerate(self.sheets):
            rt += "{num}. {sheetName}\n".format(
                num=str(i),
                sheetName=sheet.name
            )
        if not rt:
            rt = "empty book"
        print(rt)
