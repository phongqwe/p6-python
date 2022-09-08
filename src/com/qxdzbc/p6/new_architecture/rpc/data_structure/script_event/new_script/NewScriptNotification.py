from dataclasses import dataclass

from com.qxdzbc.p6.new_architecture.rpc.data_structure.common.ErrorIndicator import \
    ErrorIndicator

from com.qxdzbc.p6.document_structure.script.ScriptEntry import ScriptEntry



from com.qxdzbc.p6.document_structure.util.ToProto import ToProto
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
