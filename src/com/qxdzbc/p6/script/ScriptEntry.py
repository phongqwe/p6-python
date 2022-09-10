from dataclasses import dataclass

from com.qxdzbc.p6.util.ToProto import ToProto
from com.qxdzbc.p6.workbook.key.WorkbookKey import WorkbookKey
from com.qxdzbc.p6.script.ScriptEntryKey import ScriptEntryKey
from com.qxdzbc.p6.proto.ScriptProtos_pb2 import ScriptEntryProto

@dataclass
class ScriptEntry(ToProto[ScriptEntryProto]):
    key:ScriptEntryKey
    script:str = ""

    @staticmethod
    def fromProto(proto:ScriptEntryProto)->'ScriptEntry':
        return ScriptEntry(
            key = ScriptEntryKey.fromProto(proto.key),
            script=proto.script
        )

    def toProtoObj(self) -> ScriptEntryProto:
        return ScriptEntryProto(
            key = self.key.toProtoObj(),
            script = self.script
        )

    def setWorkbookKey(self,workbookKey:WorkbookKey)->'ScriptEntry':
        newKey = self.key.setWorkbookKey(workbookKey)
        self.key = newKey
        return self

    def setScript(self,newScript:str)->'ScriptEntry':
        self.script = newScript
        return self
