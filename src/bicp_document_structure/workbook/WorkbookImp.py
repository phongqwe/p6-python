from pathlib import Path
from typing import Union, Optional, Tuple

from bicp_document_structure.formula_translator.FormulaTranslator import FormulaTranslator
from bicp_document_structure.formula_translator.FormulaTranslators import FormulaTranslators
from bicp_document_structure.util.CommonError import CommonErrors
from bicp_document_structure.util.Util import typeCheck
from bicp_document_structure.util.report.error.ErrorReport import ErrorReport
from bicp_document_structure.util.result.Err import Err
from bicp_document_structure.util.result.Ok import Ok
from bicp_document_structure.util.result.Result import Result
from bicp_document_structure.util.result.Results import Results
from bicp_document_structure.workbook.WorkBook import Workbook
from bicp_document_structure.workbook.WorkbookErrors import WorkbookErrors
from bicp_document_structure.workbook.key.WorkbookKey import WorkbookKey
from bicp_document_structure.workbook.key.WorkbookKeyImp import WorkbookKeyImp
from bicp_document_structure.workbook.key.WorkbookKeys import WorkbookKeys
from bicp_document_structure.worksheet.Worksheet import Worksheet
from bicp_document_structure.worksheet.WorksheetErrors import WorksheetErrors
from bicp_document_structure.worksheet.WorksheetImp import WorksheetImp
from bicp_document_structure.worksheet.WorksheetWrapper import WorksheetWrapper


class WorkbookImp(Workbook):

    def __init__(self, name: str,
                 path: Path = None,
                 sheetList: list[Worksheet] = None,
                 ):
        self.__key = WorkbookKeyImp(name, path)
        if sheetList is None:
            sheetList = []
        else:
            typeCheck(sheetList, "sheetDict", list)
        self._sheetList: list[Worksheet] = sheetList
        self._sheetDictByName: dict[str, Worksheet] = {}
        for sheet in self._sheetList:
            self._sheetDictByName[sheet.name] = sheet

        self.__activeSheet = None
        if self.sheetCount != 0:
            self.__activeSheet = self._sheetList[0]
        self.__nameCount = 0

        # translator dict key = [sheetName, workbook key]
        self._translatorDict: dict[Tuple[str, WorkbookKey], FormulaTranslator] = {}

    ### >> Workbook << ###

    def getTranslator(self, sheetName: str) -> FormulaTranslator:
        if self.haveSheet(sheetName):
            key = (sheetName, self.__key)
            rt: FormulaTranslator | None = self._translatorDict.get(key)
            if rt is None:
                self._translatorDict[key] = FormulaTranslators.standardWbWs(sheetName, self.__key)
                rt = self._translatorDict[key]
            return rt
        else:
            raise Exception(
                f'Workbook \'{self.name}\' does not contain sheet \'{sheetName}\', therefore it cannot provide a translator for that sheet.')

    @property
    def worksheets(self) -> list[Worksheet]:
        return self._sheetList

    @property
    def workbookKey(self) -> WorkbookKey:
        return self.__key

    @workbookKey.setter
    def workbookKey(self, newKey: WorkbookKey):
        self.__key = newKey
        # translators depend on workbook key,
        # therefore when workbook key is changed, all the old translators must be removed
        self._translatorDict = {}

    def setActiveWorksheet(self, indexOrName: Union[int, str]):
        sheet = self.getWorksheet(indexOrName)
        if sheet is not None:
            # need to remove the event layer
            if isinstance(sheet, WorksheetWrapper):
                self.__activeSheet = sheet.innerSheet
            else:
                self.__activeSheet = sheet
        else:
            raise ValueError("{n} is invalid workbook index or workbook".format(n = indexOrName))

    @property
    def activeWorksheet(self) -> Optional[Worksheet]:
        if not self.isEmpty() and self.__activeSheet is None:
            self.__activeSheet = self.getWorksheetByIndex(0)
        return self.__activeSheet

    def isEmpty(self) -> bool:
        return self.sheetCount == 0

    def getWorksheetByNameRs(self, name: str) -> Result[Worksheet, ErrorReport]:
        typeCheck(name, "name", str)
        ws = self._sheetDictByName.get(name)
        if ws is not None:
            return Ok(ws)
        else:
            return Err(
                ErrorReport(
                    header = WorkbookErrors.WorksheetNotExistReport.header,
                    data = WorkbookErrors.WorksheetNotExistReport.Data(name)
                )
            )

    def getWorksheetByIndexRs(self, index: int) -> Result[Worksheet, ErrorReport]:
        if 0 <= index < self.sheetCount:
            rt: Worksheet = self._sheetList[index]
            return Ok(rt)
        else:
            return Err(WorkbookErrors.WorksheetNotExistReport(index))

    def getWorksheetRs(self, nameOrIndex: Union[str, int]) -> Result[Worksheet, ErrorReport]:
        if isinstance(nameOrIndex, str):
            return self.getWorksheetByNameRs(nameOrIndex)
        elif isinstance(nameOrIndex, int):
            return self.getWorksheetByIndexRs(nameOrIndex)
        else:
            return Err(CommonErrors.WrongTypeReport("nameOrIndex", "str or int"))

    def getWorksheetByNameOrNone(self, name: str) -> Worksheet | None:
        return self._sheetDictByName.get(name)

    def getWorksheetByIndexOrNone(self, index: int) -> Optional[Worksheet]:
        rs = self.getWorksheetByIndexRs(index)
        return Results.extractOrNone(rs)

    def getWorksheetOrNone(self, nameOrIndex: Union[str, int]) -> Optional[Worksheet]:
        return Results.extractOrNone(self.getWorksheetByNameRs(nameOrIndex))

    def getWorksheet(self, nameOrIndex: Union[str, int]) -> Worksheet:
        rs = self.getWorksheetRs(nameOrIndex)
        return Results.extractOrRaise(rs)

    def getWorksheetByName(self, name: str) -> Worksheet:
        rs = self.getWorksheetByNameRs(name)
        return Results.extractOrRaise(rs)

    def getWorksheetByIndex(self, index: int) -> Worksheet:
        rs = self.getWorksheetByIndexRs(index)
        return Results.extractOrRaise(rs)

    def renameWorksheetRs(self, oldSheetNameOrIndex: str | int, newSheetName: str) -> Result[None, ErrorReport]:
        if len(newSheetName) == 0 or newSheetName is None:
            return Err(ErrorReport(
                header = WorksheetErrors.IllegalNameReport.header,
                data = WorksheetErrors.IllegalNameReport.Data(newSheetName)
            ))
        targetSheet: Worksheet | None = self.getWorksheetOrNone(oldSheetNameOrIndex)
        if targetSheet is None:
            return Err(ErrorReport(
                WorkbookErrors.WorksheetNotExistReport.header,
                WorkbookErrors.WorksheetNotExistReport.Data(oldSheetNameOrIndex)
            ))
        else:
            if targetSheet.name == newSheetName:
                return Ok(None)
            newNameNotMapToExistingSheet = self.getWorksheetOrNone(newSheetName) is None
            if newNameNotMapToExistingSheet:
                oldName = targetSheet.name
                targetSheet.internalRename(newSheetName)
                # update sheet dict
                self._sheetDictByName.pop(oldName)
                self._sheetDictByName[newSheetName] = targetSheet
                # update translator map
                oldTranslatorDictKey = (oldName, self.workbookKey)
                # delete old cached translator. New translator will be lazily created when it is queried.
                if oldTranslatorDictKey in self._translatorDict.keys():
                    self._translatorDict.pop(oldTranslatorDictKey)
                return Ok(None)
            else:
                return Err(ErrorReport(
                    WorkbookErrors.WorksheetAlreadyExistReport.header,
                    WorkbookErrors.WorksheetNotExistReport.Data(newSheetName)
                ))

    @property
    def sheetCount(self) -> int:
        return len(self._sheetList)

    @property
    def path(self) -> Path:
        return self.workbookKey.filePath

    @path.setter
    def path(self, newPath: Path):
        self.workbookKey = WorkbookKeys.fromNameAndPath(self.name, newPath)

    @property
    def name(self) -> str:
        return self.workbookKey.fileName

    @name.setter
    def name(self, newName: str):
        self.workbookKey = WorkbookKeys.fromNameAndPath(newName, self.workbookKey.filePath)

    def _generateNewSheetName(self) -> str:
        # TODO this generator function is inconsistent with the front end logic, fix it
        newSheetName = "Sheet" + str(self.__nameCount)
        while self.getWorksheetByNameOrNone(newSheetName) is not None:
            self.__nameCount += 1
            newSheetName = "Sheet" + str(self.__nameCount)
        return newSheetName

    def createNewWorksheetRs(self, newSheetName: Optional[str] = None) -> Result[Worksheet, ErrorReport]:
        if newSheetName is None:
            newSheetName = self._generateNewSheetName()

        if len(newSheetName) == 0:
            newSheetName = self._generateNewSheetName()

        if self.haveSheet(newSheetName):
            return Err(
                ErrorReport(
                    header = WorkbookErrors.WorksheetAlreadyExistReport.header,
                    data = WorkbookErrors.WorksheetAlreadyExistReport.Data(newSheetName)
                )
            )
        newSheet = WorksheetImp(
            name = newSheetName,
            translatorGetter = self.getTranslator, )
        # store new sheet in name map
        self._sheetDictByName[newSheetName] = newSheet
        # store in index list
        self._sheetList.append(newSheet)
        return Ok(newSheet)

    def removeWorksheetByNameRs(self, sheetName: str) -> Result[Worksheet, ErrorReport]:
        typeCheck(sheetName, "sheetName", str)
        if sheetName in self._sheetDictByName.keys():
            rt: Worksheet = self._sheetDictByName[sheetName]
            del self._sheetDictByName[sheetName]
            if rt in self._sheetList:
                self._sheetList.remove(rt)
            return Ok(rt)
        else:
            return Err(
                ErrorReport(
                    header = WorkbookErrors.WorksheetAlreadyExistReport.header,
                    data = WorkbookErrors.WorksheetAlreadyExistReport.Data(sheetName),
                )
            )

    def removeWorksheetByIndexRs(self, index: int) -> Result[Worksheet, ErrorReport]:
        typeCheck(index, "index", int)
        if 0 <= index < self.sheetCount:
            sheet: Worksheet = self._sheetList[index]
            self._sheetList.pop(index)
            name: str = sheet.name
            return self.removeWorksheetByNameRs(name)
        else:
            return Err(
                ErrorReport(
                    header = WorkbookErrors.WorksheetAlreadyExistReport.header,
                    data = WorkbookErrors.WorksheetAlreadyExistReport.Data(index),
                )
            )

    def removeWorksheetRs(self, nameOrIndex: Union[str, int]) -> Result[Worksheet, ErrorReport]:
        if isinstance(nameOrIndex, str):
            return self.removeWorksheetByNameRs(nameOrIndex)

        if isinstance(nameOrIndex, int):
            return self.removeWorksheetByIndexRs(nameOrIndex)

        raise ValueError("nameOrIndex must either be a string or a number")

    def toJsonDict(self) -> dict:
        return self.toJson().toJsonDict()
