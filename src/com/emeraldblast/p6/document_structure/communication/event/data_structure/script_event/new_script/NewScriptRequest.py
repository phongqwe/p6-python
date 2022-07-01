from dataclasses import dataclass

from com.emeraldblast.p6.document_structure.script.ScriptEntry import ScriptEntry

from com.emeraldblast.p6.document_structure.util.ToProto import ToProto
from com.emeraldblast.p6.proto.ScriptProtos_pb2 import NewScriptRequestProto

@dataclass
class NewScriptRequest(ToProto[NewScriptRequestProto]):
    scriptEntry:ScriptEntry

    @staticmethod
    def fromProtoBytes(data:bytes)->'NewScriptRequest':
        proto = NewScriptRequestProto()
        proto.ParseFromString(data)
        return NewScriptRequest(
            scriptEntry = ScriptEntry.fromProto(proto.scriptEntry)
        )
    
    @staticmethod
    def fromProto(proto:NewScriptRequestProto):
        return NewScriptRequest(
            scriptEntry = ScriptEntry.fromProto(proto.scriptEntry)
        )
    
    def toProtoObj(self) -> NewScriptRequestProto:
        rt=NewScriptRequestProto(
            scriptEntry=self.scriptEntry.toProtoObj()
        )
        return rt