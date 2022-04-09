from com.emeraldblast.p6.document_structure.communication.event.P6Event import P6Event
from com.emeraldblast.p6.document_structure.util.ToProto import ToProto


class EventData:
    def __init__(self,
                 event: P6Event = None,
                 isError: bool = False,
                 data: ToProto = None):
        self.event = event
        self.isError = isError
        self.data = data
