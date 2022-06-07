from com.emeraldblast.p6.document_structure.communication.event.P6Event import P6Event
from com.emeraldblast.p6.document_structure.util.ToProto import ToProto
from com.emeraldblast.p6.document_structure.util.report.error.ErrorReport import ErrorReport
from com.emeraldblast.p6.document_structure.util.result.Result import Result


class EventData:
    def __init__(self,
                 event: P6Event,
                 isError: bool = False,
                 data: ToProto|bytes = b""):
        self.event = event
        self.isError = isError
        self.data = data
        
    @staticmethod
    def fromToProtoRs(event:P6Event,rs: Result[ToProto, ErrorReport]):
        eventData = EventData(
            event = event,
            isError = rs.isErr(),
        )
        if rs.isOk():
            eventData.data = rs.value.toProtoBytes()
        if rs.isErr():
            eventData.data = rs.err.toProtoBytes()
        return eventData

    def __eq__(self, other):
        if isinstance(other,EventData):
            sameEvent=self.event == other.event
            sameErr = self.isError == other.isError
            sameData = self.data == other.data
            return sameEvent and sameErr and sameData
        else:
            return False
