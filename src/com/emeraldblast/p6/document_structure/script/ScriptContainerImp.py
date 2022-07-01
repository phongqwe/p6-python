from com.emeraldblast.p6.document_structure.script.ScriptContainerErrors import ScriptContainerErrors
from com.emeraldblast.p6.document_structure.script.SimpleScriptEntry import SimpleScriptEntry
from com.emeraldblast.p6.document_structure.script.ScriptContainer import ScriptContainer
from com.emeraldblast.p6.document_structure.script.ScriptEntry import ScriptEntry
from com.emeraldblast.p6.document_structure.script.ScriptEntryKey import ScriptEntryKey
from com.emeraldblast.p6.document_structure.util.Util import replaceKey
from com.emeraldblast.p6.document_structure.util.WithSize import WithSize
from com.emeraldblast.p6.document_structure.util.report.error.ErrorReport import ErrorReport
from com.emeraldblast.p6.document_structure.util.result.Err import Err
from com.emeraldblast.p6.document_structure.util.result.Ok import Ok
from com.emeraldblast.p6.document_structure.util.result.Result import Result
from com.emeraldblast.p6.document_structure.util.result.Results import Results


class ScriptContainerImp(ScriptContainer, WithSize):

    def contains(self, scriptName: str) -> bool:
        return scriptName in self.scriptMap.keys()

    def renameScript(self, oldName: str, newName: str):
        newMap = replaceKey(self.scriptMap, oldName,newName)
        self.scriptMap = newMap
        return self

    @property
    def size(self) -> int:
        return len(self.scriptMap)

    def __init__(self, scriptMap: dict[str, str] | None = None):
        if scriptMap is None:
            scriptMap = {}
        self.scriptMap = scriptMap

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

    def addScriptEntry(self, entry:SimpleScriptEntry) -> 'ScriptContainer':
        self.scriptMap[entry.name] = entry.script
        return self

    def getScript(self, name: str) -> str | None:
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
