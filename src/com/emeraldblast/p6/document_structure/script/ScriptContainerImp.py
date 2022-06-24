from abc import ABC
from dataclasses import dataclass

from com.emeraldblast.p6.document_structure.script.ScriptContainer import ScriptContainer
from com.emeraldblast.p6.document_structure.script.ScriptEntry import ScriptEntry
from com.emeraldblast.p6.document_structure.script.ScriptEntryKey import ScriptEntryKey
from com.emeraldblast.p6.document_structure.util.Util import default
from com.emeraldblast.p6.document_structure.workbook.key.WorkbookKey import WorkbookKey


@dataclass
class ScriptContainerImp(ScriptContainer):
    def __init__(self, appScriptMap: dict[ScriptEntryKey, ScriptEntry] | None = None,
                 wbScriptMap: dict[WorkbookKey, dict[str, ScriptEntry]] | None = None):

        if appScriptMap is None:
            appScriptMap = {}
        if wbScriptMap is None:
            wbScriptMap = {}

        self.appScriptMap: dict[ScriptEntryKey, ScriptEntry] = appScriptMap
        self.wbScriptMap: dict[WorkbookKey, dict[str, ScriptEntry]] = wbScriptMap

    def addScript(self, scriptEntry: ScriptEntry) -> 'ScriptContainer':
        key = scriptEntry.key
        if key.workbookKey:
            wbKey = key.workbookKey
            subDict = default(self.wbScriptMap.get(wbKey), {})
            subDict[key.name] = scriptEntry
            self.wbScriptMap[wbKey] = subDict
        else:
            self.appScriptMap[key] = scriptEntry
        return self

    def getScript(self, key: ScriptEntryKey) -> ScriptEntry|None:
        if key.workbookKey:
            subMap = self.wbScriptMap.get(key.workbookKey)
            if subMap:
                return subMap.get(key.name)
            else:
                return None
        else:
            return self.appScriptMap.get(key)

    def getScriptsOfWb(self, wbKey: WorkbookKey) -> list[ScriptEntry]:
        rt= default(self.wbScriptMap.get(wbKey),{})
        return list(rt.values())

    def removeScript(self, scriptKey: ScriptEntryKey) -> 'ScriptContainer':
        raise NotImplementedError()

    def removeScriptOfWb(self, wbKey: WorkbookKey) -> 'ScriptContainer':
        raise NotImplementedError()
