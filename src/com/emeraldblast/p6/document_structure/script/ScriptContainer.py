from abc import ABC

from com.emeraldblast.p6.document_structure.script.ScriptEntry import ScriptEntry
from com.emeraldblast.p6.document_structure.script.ScriptEntryKey import ScriptEntryKey
from com.emeraldblast.p6.document_structure.workbook.key.WorkbookKey import WorkbookKey


class ScriptContainer(ABC):
    def addScript(self, scriptEntry: ScriptEntry) -> 'ScriptContainer':
        raise NotImplementedError()

    def getScript(self, key: ScriptEntryKey) -> ScriptEntry | None:
        raise NotImplementedError()

    def removeScript(self, scriptKey: ScriptEntryKey) -> 'ScriptContainer':
        raise NotImplementedError()

    def removeAll(self) -> 'ScriptContainer':
        raise NotImplementedError()

    def addAllScripts(self,scripts:list[ScriptEntry])->'ScriptContainer':
        raise NotImplementedError()

    @property
    def allScripts(self) -> list[ScriptEntry]:
        raise NotImplementedError()