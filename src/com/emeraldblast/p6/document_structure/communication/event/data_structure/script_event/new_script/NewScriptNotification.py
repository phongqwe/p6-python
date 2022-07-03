from dataclasses import dataclass

from com.emeraldblast.p6.document_structure.communication.event.data_structure.common.ErrorIndicator import \
    ErrorIndicator

from com.emeraldblast.p6.document_structure.script.ScriptEntry import ScriptEntry

from com.emeraldblast.p6.document_structure.communication.event.data_structure.ToEventData import ToEventData

from com.emeraldblast.p6.document_structure.util.ToProto import ToProto, P
from com.emeraldblast.p6.proto.ScriptProtos_pb2 import NewScriptNotificationProto


@dataclass
class NewScriptNotification(ToEventData, ToProto[NewScriptNotificationProto]):
    scriptEntries: list[ScriptEntry]
    errorIndicator: ErrorIndicator

    def toProtoObj(self) -> NewScriptNotificationProto:
        scriptEntries = list(map(lambda s:s.toProtoObj(), self.scriptEntries))
        proto = NewScriptNotificationProto(
            scriptEntries = scriptEntries,
            errorIndicator = self.errorIndicator.toProtoObj()
        )
        return proto
