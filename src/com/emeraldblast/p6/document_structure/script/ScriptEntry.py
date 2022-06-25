from dataclasses import dataclass

from com.emeraldblast.p6.document_structure.script.ScriptEntryKey import ScriptEntryKey
from com.emeraldblast.p6.document_structure.util.ToProto import ToProto, P
from com.emeraldblast.p6.document_structure.workbook.key.WorkbookKey import WorkbookKey
from com.emeraldblast.p6.proto.ScriptProtos_pb2 import ScriptEntryProto

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
