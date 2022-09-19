from dataclasses import dataclass

from com.qxdzbc.p6.script.ScriptEntry import ScriptEntry

from com.qxdzbc.p6.util.ToProto import ToProto
from com.qxdzbc.p6.rpc.data_structure.ErrorIndicator import \
    ErrorIndicator
from com.qxdzbc.p6.proto.ScriptProtos_pb2 import NewScriptNotificationProto


@dataclass
class NewScriptNotification( ToProto[NewScriptNotificationProto]):
    scriptEntries: list[ScriptEntry]
    errorIndicator: ErrorIndicator

    def toProtoObj(self) -> NewScriptNotificationProto:
        scriptEntries = list(map(lambda s:s.toProtoObj(), self.scriptEntries))
        proto = NewScriptNotificationProto(
            scriptEntries = scriptEntries,
            errorIndicator = self.errorIndicator.toProtoObj()
        )
        return proto
