from bicp_document_structure.communication.proto.CommonProtos_pb2 import NullableString


class ProtoUtils:
    @staticmethod
    def isNullStr(protoNullableString:NullableString):
        return "null" == protoNullableString.WhichOneof("kind")

    @staticmethod
    def isValidStr(protoNullableString: NullableString):
        return "str" == protoNullableString.WhichOneof("kind")