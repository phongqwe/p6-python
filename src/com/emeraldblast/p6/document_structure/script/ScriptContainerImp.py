from com.emeraldblast.p6.document_structure.script.ScriptContainer import ScriptContainer
from com.emeraldblast.p6.document_structure.script.ScriptEntry import ScriptEntry
from com.emeraldblast.p6.document_structure.script.ScriptEntryKey import ScriptEntryKey


class ScriptContainerImp(ScriptContainer):
    def addAllScripts(self, scripts: list[ScriptEntry]) -> ScriptContainer:
        s = self
        for script in scripts:
            s = s.addScript(script)
        return s

    @property
    def allScripts(self) -> list[ScriptEntry]:
        return list(self.appScriptMap.values())

    def __init__(self, appScriptMap: dict[ScriptEntryKey, ScriptEntry] | None = None):
        if appScriptMap is None:
            appScriptMap = {}
        self.appScriptMap: dict[ScriptEntryKey, ScriptEntry] = appScriptMap

    def removeAll(self) -> 'ScriptContainer':
        self.appScriptMap = {}
        return self

    def addScript(self, scriptEntry: ScriptEntry) -> 'ScriptContainer':
        self.appScriptMap[scriptEntry.key] = scriptEntry
        return self

    def getScript(self, key: ScriptEntryKey) -> ScriptEntry | None:
        return self.appScriptMap.get(key)

    def removeScript(self, scriptKey: ScriptEntryKey) -> 'ScriptContainer':
        if scriptKey in self.appScriptMap:
            self.appScriptMap.pop(scriptKey)
        return self
