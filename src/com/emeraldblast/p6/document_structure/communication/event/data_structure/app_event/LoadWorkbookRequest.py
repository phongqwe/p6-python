from pathlib import Path

from com.emeraldblast.p6.proto.AppEventProtos_pb2 import LoadWorkbookRequestProto


class LoadWorkbookRequest:
    def __init__(self,path:str, windowId:str):
        self.path=path
        self.windowId=windowId

    @property
    def absolutePath(self)->Path:
        return Path(self.path).absolute()

    @staticmethod
    def fromProtoByte(data:bytes)->'LoadWorkbookRequest':
        proto = LoadWorkbookRequestProto()
        proto.ParseFromString(data)
        return LoadWorkbookRequest(proto.path, proto.windowId)