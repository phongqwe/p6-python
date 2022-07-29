from pathlib import Path
from typing import Union, Optional, Tuple

from com.emeraldblast.p6.document_structure.formula_translator.FormulaTranslator import FormulaTranslator
from com.emeraldblast.p6.document_structure.formula_translator.FormulaTranslators import FormulaTranslators
from com.emeraldblast.p6.document_structure.script import SimpleScriptEntry
from com.emeraldblast.p6.document_structure.script.ScriptContainer import ScriptContainer
from com.emeraldblast.p6.document_structure.script.ScriptContainer import ScriptContainer
from com.emeraldblast.p6.document_structure.script.ScriptContainerImp import ScriptContainerImp
from com.emeraldblast.p6.document_structure.script.ScriptContainerImp import ScriptContainerImp
from com.emeraldblast.p6.document_structure.script.ScriptEntry import ScriptEntry
from com.emeraldblast.p6.document_structure.script.ScriptEntryKey import ScriptEntryKey
from com.emeraldblast.p6.document_structure.util.CommonError import CommonErrors
from com.emeraldblast.p6.document_structure.util.Util import typeCheck
from com.emeraldblast.p6.document_structure.util.report.error.ErrorReport import ErrorReport
from com.emeraldblast.p6.document_structure.util.result.Err import Err
from com.emeraldblast.p6.document_structure.util.result.Ok import Ok
from com.emeraldblast.p6.document_structure.util.result.Result import Result
from com.emeraldblast.p6.document_structure.workbook.WorkBook import Workbook
from com.emeraldblast.p6.document_structure.workbook.WorkbookErrors import WorkbookErrors
from com.emeraldblast.p6.document_structure.workbook.key.WorkbookKey import WorkbookKey
from com.emeraldblast.p6.document_structure.workbook.key.WorkbookKeyImp import WorkbookKeyImp
from com.emeraldblast.p6.document_structure.workbook.key.WorkbookKeys import WorkbookKeys
from com.emeraldblast.p6.document_structure.worksheet.Worksheet import Worksheet
from com.emeraldblast.p6.document_structure.worksheet.WorksheetImp import WorksheetImp


class WorkbookImp(Workbook):

    def removeScriptRs(self, name: str) -> Result[None, ErrorReport]:
        # TODO this is a place holder for future checking
        self._scriptCont = self._scriptCont.removeScript(name)
        return Ok(None)

    def addAllScriptsRs(self, scripts: list[SimpleScriptEntry]) -> Result[None, ErrorReport]:
        rs = self._scriptCont.addAllScriptsRs(scripts)
        if rs.isOk():
            self._scriptCont = rs.value
            return Ok(None)
        else:
            return Err(rs.err)

    def overwriteScriptRs(self, name: str, newScript: str) -> Result[None, ErrorReport]:
        rs = self._scriptCont.overwriteScriptRs(name, newScript)
        if rs.isOk():
            self._scriptCont = rs.value
            return Ok(None)
        else:
            return Err(rs.err)

    def overwriteScript(self, name: str, newScript: str):
        rs = self.overwriteScriptRs(name, newScript)
        rs.getOrRaise()

    def addScriptRs(self, name: str, script: str) -> Result[None, ErrorReport]:
        rs = self._scriptCont.addScriptRs(name, script)
        if rs.isOk():
            self._scriptCont = rs.value
            return Ok(None)
        else:
            return Err(rs.err)

    @property
    def allAsScriptEntry(self) -> list[ScriptEntry]:
        return self._scriptCont.allAsScriptEntry(self.workbookKey)


    def getScript(self, name: str) -> Optional[str]:
        return self._scriptCont.getScript(name)

    def removeAllScript(self):
        self._scriptCont = self._scriptCont.removeAll()

    def addAllScripts(self, scripts: list[SimpleScriptEntry]):
        self._scriptCont = self._scriptCont.addAllScripts(scripts)

    @property
    def allScripts(self) -> list[ScriptEntry]:
        return self._scriptCont.allScripts

    @property
    def scriptContainer(self) -> ScriptContainer:
        return self._scriptCont

    def __init__(
            self, name: str,
            path: Path = None,
            sheetList: list[Worksheet] = None,
            scriptContainer: ScriptContainer | None = None,
    ):
        if scriptContainer is None:
            scriptContainer = ScriptContainerImp()
        self._scriptCont = scriptContainer

        self.__key = WorkbookKeyImp(name, path)
        if sheetList is None:
            sheetList = []
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

    def makeSavableCopy(self) -> 'Workbook':
        """a copy without workbook key"""
        return WorkbookImp(
            name = "",
            path = None,
            sheetList = self._sheetList,
            scriptContainer = self._scriptCont
        )

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
        # therefore, when workbook key is changed, all the old translators must be removed
        self._translatorDict = {}

    def setActiveWorksheetRs(self, indexOrName: Union[int, str]) -> Result[Worksheet, ErrorReport]:
        getRs = self.getWorksheetRs(indexOrName)
        if getRs.isOk():
            sheet = getRs.value
            self.__activeSheet = sheet.rootWorksheet
        return getRs

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
            return Err(WorkbookErrors.WorksheetNotExistReport(name))

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
            return Err(WorkbookErrors.WorksheetAlreadyExistReport(newSheetName))

        newSheet = WorksheetImp(
            name = newSheetName,
            workbook = self
        )
        # store new sheet in name map
        self._sheetDictByName[newSheetName] = newSheet
        # store in index list
        self._sheetList.append(newSheet)
        return Ok(newSheet)

    def deleteWorksheetByNameRs(self, sheetName: str) -> Result[Worksheet, ErrorReport]:
        typeCheck(sheetName, "sheetName", str)
        if sheetName in self._sheetDictByName.keys():
            rt: Worksheet = self._sheetDictByName[sheetName]
            del self._sheetDictByName[sheetName]
            if rt in self._sheetList:
                self._sheetList.remove(rt)
            rt.removeFromWorkbook()

            # delete old cached translator. New translator will be lazily created when it is requested.
            oldTranslatorDictKey = (sheetName, self.workbookKey)
            if oldTranslatorDictKey in self._translatorDict.keys():
                self._translatorDict.pop(oldTranslatorDictKey)
            return Ok(rt)
        else:
            return Err(WorkbookErrors.WorksheetNotExistReport(sheetName))

    def deleteWorksheetByIndexRs(self, index: int) -> Result[Worksheet, ErrorReport]:
        typeCheck(index, "index", int)
        if 0 <= index < self.sheetCount:
            sheet: Worksheet = self._sheetList[index]
            self._sheetList.pop(index)
            return self.deleteWorksheetByNameRs(sheet.name)
        else:
            return Err(WorkbookErrors.WorksheetNotExistReport(index))

    def addWorksheetRs(self, ws: Worksheet) -> Result[None, ErrorReport]:
        if self.haveSheet(ws.name):
            return Err(WorkbookErrors.WorksheetAlreadyExistReport(ws.name))
        else:
            # store new sheet in name map
            self._sheetDictByName[ws.name] = ws
            # store in index list
            self._sheetList.append(ws)
            # wire the ws to this wb
            ws.workbook = self
            return Ok(None)

    def toJsonDict(self) -> dict:
        return self.toJson().toJsonDict()

    def changeSheetName(self, oldName: str, ws: Worksheet):
        if ws in self.worksheets:
            self._sheetDictByName.pop(oldName)
            self._sheetDictByName[ws.name] = ws

            translatorKey = (oldName, self.workbookKey)
            if translatorKey in self._translatorDict.keys():
                self._translatorDict.pop(translatorKey)
        else:
            self.addWorksheet(ws)

    @property
    def rootWorkbook(self) -> 'Workbook':
        return self
