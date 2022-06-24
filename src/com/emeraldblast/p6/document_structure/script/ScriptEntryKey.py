from dataclasses import dataclass

from com.emeraldblast.p6.document_structure.util.ToProto import ToProto
from com.emeraldblast.p6.document_structure.workbook.key.WorkbookKey import WorkbookKey
from com.emeraldblast.p6.document_structure.workbook.key.WorkbookKeys import WorkbookKeys
from com.emeraldblast.p6.proto.ScriptProtos_pb2 import ScriptEntryKeyProto

@dataclass
class ScriptEntryKey(ToProto[ScriptEntryKeyProto]):
    name:str
    workbookKey:WorkbookKey|None

    @staticmethod
    def fromProto(proto:ScriptEntryKeyProto)->'ScriptEntryKey':
        wbKey = None
        if proto.HasField("workbookKey"):
            wbKey = WorkbookKeys.fromProto(proto.workbookKey)
        return ScriptEntryKey(
            name = proto.name,
            workbookKey = wbKey
        )


    def toProtoObj(self) -> ScriptEntryKeyProto:
        proto = ScriptEntryKeyProto(
            name = self.name
        )
        if self.workbookKey:
            proto.workbookKey.CopyFrom(self.workbookKey.toProtoObj())
        return proto
