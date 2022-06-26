from com.emeraldblast.p6.document_structure.script import SimpleScriptEntry
from com.emeraldblast.p6.document_structure.script.ScriptContainer import ScriptContainer
from com.emeraldblast.p6.document_structure.script.ScriptEntry import ScriptEntry
from com.emeraldblast.p6.document_structure.script.ScriptEntryKey import ScriptEntryKey
from com.emeraldblast.p6.document_structure.util.Util import replaceKey
from com.emeraldblast.p6.document_structure.util.WithSize import WithSize


class ScriptContainerImp(ScriptContainer, WithSize):

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

    def addScript(self, name: str, script: str) -> 'ScriptContainer':
        self.scriptMap[name] = script
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
        return list(self.scriptMap.values())

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
