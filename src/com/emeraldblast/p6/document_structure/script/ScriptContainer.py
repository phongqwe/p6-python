from abc import ABC

from com.emeraldblast.p6.document_structure.script import SimpleScriptEntry
from com.emeraldblast.p6.document_structure.script.ScriptEntry import ScriptEntry
from com.emeraldblast.p6.document_structure.util.report.error.ErrorReport import ErrorReport
from com.emeraldblast.p6.document_structure.util.result.Result import Result


class ScriptContainer(ABC):

    def contains(self, scriptName:str) -> bool:
        raise NotImplementedError()

    def addScriptEntry(self, entry: SimpleScriptEntry) -> 'ScriptContainer':
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

    @property
    def allScripts(self) -> list[SimpleScriptEntry]:
        raise NotImplementedError()

    def allAsScriptEntry(self, wbKey) -> list[ScriptEntry]:
        raise NotImplementedError()

    def renameScript(self, oldName: str, newName: str) -> 'ScriptContainer':
        raise NotImplementedError()
