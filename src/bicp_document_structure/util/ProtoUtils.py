from bicp_document_structure.message.proto.Common_pb2 import NullableString


class ProtoUtils:
    @staticmethod
    def toProtoStr(protoObj) -> str:
        """convert a proto object to a normal string, this string cannot be parsed by proto classes"""
        return str(protoObj.SerializeToString(), "utf-8")

    @staticmethod
    def byteProtoFromStr(protStr: str):
        """convert a string hold proto data to byte array. The result can be parsed directly by proto class"""
        return bytes(protStr, "utf-8")

    @staticmethod
    def isNullStr(protoNullableString:NullableString):
        return "null" == protoNullableString.WhichOneof("kind")

    @staticmethod
    def isValidStr(protoNullableString: NullableString):
        return "str" == protoNullableString.WhichOneof("kind")