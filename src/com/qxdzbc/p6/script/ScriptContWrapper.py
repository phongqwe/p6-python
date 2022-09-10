from com.qxdzbc.p6.script import SimpleScriptEntry
from com.qxdzbc.p6.script.ScriptContainer import ScriptContainer
from com.qxdzbc.p6.script.ScriptEntry import ScriptEntry
from com.qxdzbc.p6.util.report.error.ErrorReport import ErrorReport
from com.qxdzbc.p6.util.result.Ok import Ok
from com.qxdzbc.p6.util.result.Result import Result
from com.qxdzbc.p6.workbook.key.WorkbookKey import WorkbookKey


class ScriptContWrapper(ScriptContainer):
    """
    TODO this may not be needed
    """

    def overwriteScriptRs(self, name: str, newScript: str) -> Result['ScriptContainer',ErrorReport]:
        rs = self._rc.overwriteScriptRs(name,newScript)
        if rs.isOk():
            self._rc = rs.value
            return Ok(self)
        else:
            return rs

    def overwriteScript(self, name: str, newScript: str) -> 'ScriptContainer':
        self._rc = self._rc.overwriteScript(name, newScript)
        return self

    def addAllScriptsRs(self, scripts: list[SimpleScriptEntry]) -> Result['ScriptContainer', ErrorReport]:
        rs = self._rc.addAllScriptsRs(scripts)
        if rs.isOk():
            self._rc = rs.value
            return Ok(self)
        else:
            return rs

    @property
    def size(self) -> int:
        return self.rootCont.size

    def __init__(self, innerCont: ScriptContainer):
        self._rc = innerCont

    def addScriptEntryRs(self, entry: SimpleScriptEntry) -> Result['ScriptContainer', ErrorReport]:
        return self.rootCont.addScriptEntryRs(entry)

    @property
    def rootCont(self) -> ScriptContainer:
        return self._rc.rootCont

    def contains(self, scriptName: str) -> bool:
        return self.rootCont.contains(scriptName)

    def addScriptEntry(self, entry: SimpleScriptEntry) -> 'ScriptContainer':
        self._rc = self._rc.addScriptEntry(entry)
        return self

    def addScriptRs(self, name: str, script: str) -> Result['ScriptContainer', ErrorReport]:
        rs = self.rootCont.addScriptRs(name, script)
        if rs.isOk():
            return Ok(self)
        else:
            return rs

    def addScript(self, name: str, script: str) -> 'ScriptContainer':
        self._rc = self._rc.addScript(name, script)
        return self

    def getScript(self, name: str) -> Optional[str]:
        return self.rootCont.getScript(name)

    def removeScript(self, name: str) -> 'ScriptContainer':
        self._rc = self._rc.removeScript(name)
        return self

    def removeAll(self) -> 'ScriptContainer':
        self._rc = self._rc.removeAll()
        return self

    def addAllScripts(self, scripts: list[SimpleScriptEntry]) -> 'ScriptContainer':
        self._rc = self._rc.addAllScripts(scripts)
        return self

    @property
    def allScripts(self) -> list[SimpleScriptEntry]:
        return self.rootCont.allScripts

    def allAsScriptEntry(self, wbKey: WorkbookKey) -> list[ScriptEntry]:
        return self.rootCont.allAsScriptEntry(wbKey)

    def renameScript(self, oldName: str, newName: str) -> 'ScriptContainer':
        return self.rootCont.renameScript(oldName, newName)
