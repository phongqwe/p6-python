import google.protobuf.empty_pb2 as empty_pb2
from google.protobuf import wrappers_pb2 as wrappers



class RpcValues:
    Empty = empty_pb2.Empty()
    Int64Value = wrappers.Int64Value
    @staticmethod
    def int64(i:int):
        return RpcValues.Int64Value(value=123)