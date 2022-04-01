from bicp_document_structure.util.ToProto import ToProto, P

from bicp_document_structure.communication.proto.P6MsgPM_pb2 import P6EventProto


class P6Event(ToProto[P6EventProto]):
    """
        P6Event needs to be this complex because in the future, there will be a needed for coded events
    """

    def toProtoObj(self) -> P6EventProto:
        rt = P6EventProto()
        rt.code = self.code
        rt.name = self.name
        return rt

    def __init__(self, code:str, name:str= ""):
        self._code = code
        self._name = name

    @property
    def name(self):
        return self._name

    @property
    def code(self):
        return self._code

    def __hash__(self):
        return hash(self.code)

    def __eq__(self, other):
        if isinstance(other, P6Event):
            return self.code == other.code
        else:
            return False
