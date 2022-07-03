from abc import ABC

from com.emeraldblast.p6.document_structure.script import SimpleScriptEntry
from com.emeraldblast.p6.document_structure.script.ScriptEntry import ScriptEntry
from com.emeraldblast.p6.document_structure.util.WithSize import WithSize
from com.emeraldblast.p6.document_structure.util.report.error.ErrorReport import ErrorReport
from com.emeraldblast.p6.document_structure.util.result.Result import Result


class ScriptContainer(WithSize,ABC):

    def overwriteScript(self, name:str, newScript:str)->'ScriptContainer':
        raise NotImplementedError()
    
    def overwriteScriptRs(self, name:str, newScript:str)->Result['ScriptContainer',ErrorReport]:
        raise NotImplementedError()

    @property
    def rootCont(self) -> 'ScriptContainer':
        raise NotImplementedError()

    def contains(self, scriptName:str) -> bool:
        raise NotImplementedError()

    def addScriptEntry(self, entry: SimpleScriptEntry) -> 'ScriptContainer':
        raise NotImplementedError()

    def addScriptEntryRs(self, entry: SimpleScriptEntry) -> Result['ScriptContainer',ErrorReport]:
        raise NotImplementedError()

    def addScriptRs(self, name: str, script: str) -> Result['ScriptContainer',ErrorReport]:
        raise NotImplementedError()

    def addScript(self, name: str, script: str) -> 'ScriptContainer':
        raise NotImplementedError()

    def getScript(self, name: str) -> str | None:
        raise NotImplementedError()

    def removeScript(self, name: str) -> 'ScriptContainer':
        raise NotImplementedError()

    def removeAll(self) -> 'ScriptContainer':
        raise NotImplementedError()

    def addAllScripts(self, scripts: list[SimpleScriptEntry]) -> 'ScriptContainer':
        raise NotImplementedError()
    
    def addAllScriptsRs(self, scripts: list[SimpleScriptEntry]) -> Result['ScriptContainer',ErrorReport]:
        raise NotImplementedError()

    @property
    def allScripts(self) -> list[SimpleScriptEntry]:
        raise NotImplementedError()

    def allAsScriptEntry(self, wbKey) -> list[ScriptEntry]:
        raise NotImplementedError()

    def renameScript(self, oldName: str, newName: str) -> 'ScriptContainer':
        raise NotImplementedError()
