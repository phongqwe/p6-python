from com.qxdzbc.p6.document_structure.communication.event.P6Event import P6Event
from com.qxdzbc.p6.document_structure.util.ToProto import ToProto
from com.qxdzbc.p6.document_structure.util.report.error.ErrorReport import ErrorReport
from com.qxdzbc.p6.document_structure.util.result.Result import Result


class EventData:
    def __init__(self,
                 event: P6Event,
                 data: ToProto):
        self.event = event
        self.data = data

    def __eq__(self, other):
        if isinstance(other,EventData):
            sameEvent=self.event == other.event
            sameData = self.data == other.data
            return sameEvent and sameData
        else:
            return False
