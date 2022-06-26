from com.emeraldblast.p6.document_structure.util.ToProto import ToProto
from com.emeraldblast.p6.proto.DocProtos_pb2 import SimpleScriptEntryProto


class SimpleScriptEntry(ToProto[SimpleScriptEntryProto]):
    def __init__(self,name:str,script:str):
        self.script = script
        self.name = name


    def toProtoObj(self) -> SimpleScriptEntryProto:
        return SimpleScriptEntryProto(
            name = self.name,
            script = self.script
        )

    @staticmethod
    def fromProto(proto:SimpleScriptEntryProto)->'SimpleScriptEntry':
        return SimpleScriptEntry(
            name = proto.name,
            script = proto.script
        )




    def __eq__(self, o: object) -> bool:
        if isinstance(o, SimpleScriptEntry):
            return self.script == o.script and self.name == o.name
        else:
            return False

    def __hash__(self):
        return hash((self.name,self.script))

