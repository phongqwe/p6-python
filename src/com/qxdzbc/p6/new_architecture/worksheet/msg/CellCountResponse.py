from com.qxdzbc.p6.document_structure.util.ToProto import ToProto
from com.qxdzbc.p6.proto.WorksheetProtos_pb2 import CellCountResponseProto


class CellCountResponse(ToProto[CellCountResponseProto]):
    def __init__(self, count:int):
        self.count = count


    @staticmethod
    def fromProto(o:CellCountResponseProto)->'CellCountResponse':
        return CellCountResponse(
            count = o.count
        )

    def toProtoObj(self) -> CellCountResponseProto:
        return CellCountResponseProto(count=self.count)

