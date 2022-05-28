from com.emeraldblast.p6.document_structure.workbook.key.WorkbookKey import WorkbookKey
from com.emeraldblast.p6.document_structure.workbook.key.WorkbookKeys import WorkbookKeys
from com.emeraldblast.p6.proto.AppEventProtos_pb2 import CloseWorkbookRequestProto


class CloseWorkbookRequest:
    def __init__(self, workbookKey:WorkbookKey,windowId:str|None,):
        self.windowId = windowId
        self.workbookKey = workbookKey
    
    @staticmethod
    def fromProtoBytes(data:bytes)->'CloseWorkbookRequest':
        proto = CloseWorkbookRequestProto()
        proto.ParseFromString(data)
        wid = None
        if proto.HasField("windowId"):
            wid = proto.windowId

        rt= CloseWorkbookRequest(
            workbookKey = WorkbookKeys.fromProto(proto.workbookKey),
            windowId = wid
        )
        return rt
        
