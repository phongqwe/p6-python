from dataclasses import dataclass

from com.emeraldblast.p6.document_structure.util.ToProto import ToProto, P
from com.emeraldblast.p6.proto.P6FileProtos_pb2 import ScriptInFileProto

@dataclass
class ScriptInFile(ToProto[ScriptInFileProto]):
    name:str
    script:str

    def toProtoObj(self) -> ScriptInFileProto:
        return ScriptInFileProto(
            name = self.name,
            script = self.script
        )

    @staticmethod
    def fromProto(proto:ScriptInFileProto)->'ScriptInFile':
        return ScriptInFile(
            name = proto.name,
            script = proto.script
        )


