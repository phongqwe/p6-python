from collections import OrderedDict as ODict
from pathlib import Path
from typing import Union, Optional, OrderedDict, Tuple

from bicp_document_structure.formula_translator.FormulaTranslator import FormulaTranslator
from bicp_document_structure.formula_translator.FormulaTranslators import FormulaTranslators
from bicp_document_structure.util.Util import typeCheck
from bicp_document_structure.util.report.error.ErrorReport import ErrorReport
from bicp_document_structure.util.result.Err import Err
from bicp_document_structure.util.result.Ok import Ok
from bicp_document_structure.util.result.Result import Result
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

    def getWorksheetByName(self, name: str) -> Optional[Worksheet]:
        typeCheck(name, "name", str)
        if name in self._sheetDictByName.keys():
            return self._sheetDictByName[name]
        else:
            return None

    def getWorksheetByIndex(self, index: int) -> Optional[Worksheet]:
        typeCheck(index, "index", int)
        if 0 <= index < self.sheetCount:
            rt: Worksheet = self._sheetList[index]
            return rt
        else:
            return None

    def renameWorksheetRs(self, oldSheetNameOrIndex: str | int, newSheetName: str) -> Result[None, ErrorReport]:
        if len(newSheetName) == 0 or newSheetName is None:
            return Err(ErrorReport(
                header = WorksheetErrors.IllegalName.header,
                data = WorksheetErrors.IllegalName.Data(newSheetName)
            ))
        targetSheet: Worksheet | None = self.getWorksheet(oldSheetNameOrIndex)
        if targetSheet is None:
            return Err(ErrorReport(
                WorkbookErrors.WorksheetNotExist.header,
                WorkbookErrors.WorksheetNotExist.Data(oldSheetNameOrIndex)
            ))
        else:
            if targetSheet.name == newSheetName:
                return Ok(None)
            newNameNotMapToExistingSheet = self.getWorksheet(newSheetName) is None
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
                    WorkbookErrors.WorksheetAlreadyExist.header,
                    WorkbookErrors.WorksheetNotExist.Data(newSheetName)
                ))

    def getWorksheet(self, nameOrIndex: Union[str, int]) -> Optional[Worksheet]:
        if isinstance(nameOrIndex, str):
            return self.getWorksheetByName(nameOrIndex)
        elif isinstance(nameOrIndex, int):
            return self.getWorksheetByIndex(nameOrIndex)
        else:
            raise ValueError(
                "nameOrIndex is of type {t}. nameOrIndex must be string or int.".format(t = str(type(nameOrIndex))))

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
        newSheetName = "Sheet" + str(self.__nameCount)
        while self.getWorksheetByName(newSheetName) is not None:
            self.__nameCount += 1
            newSheetName = "Sheet" + str(self.__nameCount)
        return newSheetName

    def createNewWorksheetRs(self, newSheetName: Optional[str] = None) -> Result[Worksheet, ErrorReport]:
        if newSheetName is None:
            newSheetName = self._generateNewSheetName()

        if self.haveSheet(newSheetName):
            return Err(
                ErrorReport(
                    header = WorkbookErrors.WorksheetAlreadyExist.header,
                    data = WorkbookErrors.WorksheetAlreadyExist.Data(newSheetName)
                )
            )
        newSheet = WorksheetImp(
            name = newSheetName,
            translatorGetter = self.getTranslator,)
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
                    header = WorkbookErrors.WorksheetAlreadyExist.header,
                    data = WorkbookErrors.WorksheetAlreadyExist.Data(sheetName),
                )
            )

    def removeWorksheetByIndexRs(self, index: int) -> Result[Worksheet, ErrorReport]:
        typeCheck(index, "index", int)
        if 0 <= index < self.sheetCount:
            sheet:Worksheet = self._sheetList[index]
            self._sheetList.pop(index)
            name: str = sheet.name
            return self.removeWorksheetByNameRs(name)
        else:
            return Err(
                ErrorReport(
                    header = WorkbookErrors.WorksheetAlreadyExist.header,
                    data = WorkbookErrors.WorksheetAlreadyExist.Data(index),
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
