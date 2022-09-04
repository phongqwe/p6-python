from com.qxdzbc.p6.document_structure.util.ToProto import ToProto


class MockToProto(ToProto):
    """a mock implementation of ToProtoInterface"""
    def __init__(self,str):
        self.str = str
    def toProtoObj(self):
        raise NotImplementedError

    def toProtoBytes(self):
        return self.str