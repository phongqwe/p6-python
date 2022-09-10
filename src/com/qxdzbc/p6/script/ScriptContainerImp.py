from typing import Optional

from com.qxdzbc.p6.script.ScriptContainerErrors import ScriptContainerErrors
from com.qxdzbc.p6.script.SimpleScriptEntry import SimpleScriptEntry
from com.qxdzbc.p6.script.ScriptContainer import ScriptContainer
from com.qxdzbc.p6.script.ScriptEntry import ScriptEntry
from com.qxdzbc.p6.script.ScriptEntryKey import ScriptEntryKey
from com.qxdzbc.p6.util.Util import replaceKey
from com.qxdzbc.p6.util.report.error.ErrorReport import ErrorReport
from com.qxdzbc.p6.util.result.Err import Err
from com.qxdzbc.p6.util.result.Ok import Ok
from com.qxdzbc.p6.util.result.Result import Result


class ScriptContainerImp(ScriptContainer):

    def overwriteScriptRs(self, name: str, newScript: str) -> Result['ScriptContainer', ErrorReport]:
        """TODO this is a placeholder for future logic such as script name checking"""
        self.scriptMap[name] = newScript
        return Ok(self)

    def overwriteScript(self, name: str, newScript: str)->ScriptContainer:
        rs = self.overwriteScriptRs(name, newScript)
        rt = rs.getOrRaise()
        return rt

    def addAllScriptsRs(self, scripts: list[SimpleScriptEntry]) -> Result['ScriptContainer', ErrorReport]:
        illegalScriptNameList = []
        for sc in scripts:
            if self.contains(sc.name):
                illegalScriptNameList.append(sc.name)
        allScriptsAreOk = len(illegalScriptNameList) == 0
        if allScriptsAreOk:
            c = self
            for sc in scripts:
                c = c.addScriptEntry(sc)
            return Ok(c)
        else:
            return Err(ScriptContainerErrors.MultipleScriptAlreadyExist.report(illegalScriptNameList))

    def __init__(self, scriptMap: dict[str, str] | None = None):
        if scriptMap is None:
            scriptMap = {}
        self.scriptMap = scriptMap

    def addScriptEntryRs(self, entry: SimpleScriptEntry) -> Result['ScriptContainer', ErrorReport]:
        return self.addScriptRs(entry.name, entry.script)

    @property
    def rootCont(self) -> 'ScriptContainer':
        return self

    def contains(self, scriptName: str) -> bool:
        return scriptName in self.scriptMap.keys()

    def renameScript(self, oldName: str, newName: str):
        newMap = replaceKey(self.scriptMap, oldName, newName)
        self.scriptMap = newMap
        return self

    @property
    def size(self) -> int:
        return len(self.scriptMap)

    def addScriptRs(self, name: str, script: str) -> Result['ScriptContainer', ErrorReport]:
        if name in self.scriptMap.keys():
            return Err(ScriptContainerErrors.ScriptAlreadyExist.report(name))
        else:
            self.scriptMap[name] = script
            return Ok(self)

    def addScript(self, name: str, script: str) -> 'ScriptContainer':
        rs = self.addScriptRs(name, script)
        rt = rs.getOrRaise()
        return rt

    def addScriptEntry(self, entry: SimpleScriptEntry) -> 'ScriptContainer':
        rs = self.addScriptEntryRs(entry)
        rt = rs.getOrRaise()
        return rt

    def getScript(self, name: str) -> Optional[str]:
        return self.scriptMap.get(name)

    def removeScript(self, name: str) -> 'ScriptContainer':
        if name in self.scriptMap.keys():
            self.scriptMap.pop(name)
        return self

    def removeAll(self) -> 'ScriptContainer':
        self.scriptMap.clear()
        return self

    def addAllScripts(self, scripts: list[SimpleScriptEntry]) -> 'ScriptContainer':
        for e in scripts:
            self.scriptMap[e.name] = e.script
        return self

    @property
    def allScripts(self) -> list[SimpleScriptEntry]:
        rt = []
        for scriptName in self.scriptMap.keys():
            rt.append(SimpleScriptEntry(scriptName, self.scriptMap[scriptName]))
        return rt

    def allAsScriptEntry(self, wbKey) -> list[ScriptEntry]:
        rt = []
        for (name, script) in self.scriptMap.items():
            rt.append(ScriptEntry(
                key = ScriptEntryKey(
                    name = name,
                    workbookKey = wbKey
                ),
                script = script
            ))
        return rt
