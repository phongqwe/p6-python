from pathlib import Path
from typing import Union, Optional

from com.qxdzbc.p6.document_structure.formula_translator.FormulaTranslator import FormulaTranslator
from com.qxdzbc.p6.document_structure.script import SimpleScriptEntry
from com.qxdzbc.p6.document_structure.script.ScriptContainer import ScriptContainer
from com.qxdzbc.p6.document_structure.script.ScriptEntry import ScriptEntry

from com.qxdzbc.p6.document_structure.util.report.error.ErrorReport import ErrorReport
from com.qxdzbc.p6.document_structure.util.result.Result import Result
from com.qxdzbc.p6.document_structure.workbook.WorkBook import Workbook
from com.qxdzbc.p6.document_structure.workbook.key.WorkbookKey import WorkbookKey
from com.qxdzbc.p6.document_structure.worksheet.Worksheet import Worksheet


class WorkbookWrapper(Workbook):

    def addAllScriptsRs(self, scripts: list[SimpleScriptEntry]) -> Result[None, ErrorReport]:
        return self.rootWorkbook.addAllScriptsRs(scripts)

    def overwriteScriptRs(self, name: str, newScript: str) -> Result[None, ErrorReport]:
        return self.rootWorkbook.overwriteScriptRs(name, newScript)

    def getScript(self, name: str) -> Optional[str]:
        return self.rootWorkbook.getScript(name)

    def removeScriptRs(self,name: str)->Result[None,ErrorReport]:
        return self.rootWorkbook.removeScriptRs(name)

    def removeAllScript(self):
        self.rootWorkbook.removeAllScript()

    @property
    def allScripts(self) -> list[SimpleScriptEntry]:
        return self.rootWorkbook.allScripts

    @property
    def allAsScriptEntry(self) -> list[ScriptEntry]:
        return self.rootWorkbook.allAsScriptEntry

    @property
    def scriptContainer(self) -> ScriptContainer:
        return self.rootWorkbook.scriptContainer

    def makeSavableCopy(self) -> 'Workbook':
        return self.rootWorkbook.makeSavableCopy()

    @property
    def rootWorkbook(self) -> 'Workbook':
        return self._innerWorkbook.rootWorkbook

    def renameWorksheetName(self, oldName: str, ws: Worksheet):
        self.rootWorkbook.renameWorksheetName(oldName, ws)

    def addWorksheetRs(self, ws: Worksheet) -> Result[None, ErrorReport]:
        return self.rootWorkbook.addWorksheetRs(ws)

    def __init__(self, innerWorkbook: Workbook):
        self._innerWorkbook = innerWorkbook

    def getTranslator(self, sheetName: str) -> FormulaTranslator:
        return self.rootWorkbook.getTranslator(sheetName)

    @property
    def path(self) -> Path:
        return self.rootWorkbook.path

    @property
    def worksheets(self) -> list[Worksheet]:
        return self.rootWorkbook.worksheets

    @property
    def workbookKey(self) -> WorkbookKey:
        return self.rootWorkbook.key

    @workbookKey.setter
    def key(self, newKey: WorkbookKey):
        self.rootWorkbook.key = newKey

    @property
    def activeWorksheet(self) -> Optional[Worksheet]:
        return self.rootWorkbook.activeWorksheet

    @property
    def sheetCount(self) -> int:
        return self.rootWorkbook.sheetCount

    @property
    def name(self) -> str:
        return self.rootWorkbook.name

    @name.setter
    def name(self, newName):
        self.rootWorkbook.name = newName

    def createNewWorksheetRs(self, newSheetName: Optional[str] = None) -> Result[Worksheet, ErrorReport]:
        return self.rootWorkbook.createNewWorksheetRs(newSheetName)

    def deleteWorksheetByNameRs(self, sheetName: str) -> Result[Worksheet, ErrorReport]:
        return self.rootWorkbook.deleteWorksheetByNameRs(sheetName)

    def deleteWorksheetByIndexRs(self, index: int) -> Result[Worksheet, ErrorReport]:
        return self.rootWorkbook.deleteWorksheetByIndexRs(index)

    def setActiveWorksheetRs(self, indexOrName: Union[int, str]) -> Result[Worksheet, ErrorReport]:
        return self.rootWorkbook.setActiveWorksheetRs(indexOrName)

    def toJsonDict(self) -> dict:
        return self.rootWorkbook.toJsonDict()

    def isEmpty(self) -> bool:
        return self.rootWorkbook.isEmpty()

    @property
    def innerWorkbook(self):
        return self._innerWorkbook

    def __eq__(self, o: object) -> bool:
        if isinstance(o, WorkbookWrapper):
            return self._innerWorkbook == o._innerWorkbook
        elif isinstance(o, Workbook):
            return self._innerWorkbook == o
        else:
            return False

    def getWorksheetByNameRs(self, name: str) -> Result[Worksheet, ErrorReport]:
        return self.rootWorkbook.getWorksheetByNameRs(name)

    def getWorksheetByIndexRs(self, index: int) -> Result[Worksheet, ErrorReport]:
        return self.rootWorkbook.getWorksheetByIndexRs(index)

    def getWorksheetRs(self, nameOrIndex: Union[str, int]) -> Result[Worksheet, ErrorReport]:
        return self.rootWorkbook.getWorksheetRs(nameOrIndex)
