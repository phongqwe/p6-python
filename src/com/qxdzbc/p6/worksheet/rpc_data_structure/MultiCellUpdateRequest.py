from dataclasses import dataclass, field

from com.qxdzbc.p6.proto.DocProtos_pb2 import WorksheetIdProto, IndCellProto
from com.qxdzbc.p6.proto.WorksheetProtos_pb2 import MultiCellUpdateRequestProto
from com.qxdzbc.p6.util.ToProto import ToProto


@dataclass
class MultiCellUpdateRequest(ToProto[MultiCellUpdateRequestProto]):

    wsId: ToProto[WorksheetIdProto]
    updateEntries: list[ToProto[IndCellProto]] = field(default_factory = lambda: [])

    def toProtoObj(self) -> MultiCellUpdateRequestProto:
        return MultiCellUpdateRequestProto(
            wsId = self.wsId.toProtoObj(),
            updateEntries = list(map(lambda e:e.toProtoObj(),self.updateEntries))
        )