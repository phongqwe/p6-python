from com.emeraldblast.p6.proto.CellProtos_pb2 import CellUpdateContentProto


class CellUpdateContent:
    def __init__(self, formula:str, literal:str):
        self.literal = literal
        self.formula = formula

    def __eq__(self, other):
        if isinstance(other,CellUpdateContent):
            return self.literal == other.literal and self.formula == other.formula
        else:
            return False

    @staticmethod
    def fromProto(proto:CellUpdateContentProto)->'CellUpdateContent':
        rt = CellUpdateContent(
            formula = proto.formula,
            literal = proto.literal
        )
        return rt
    @staticmethod
    def fromProtoBytes(data:bytes)->'CellUpdateContent':
        proto = CellUpdateContentProto()
        proto.ParseFromString(data)
        return CellUpdateContent.fromProto(proto)