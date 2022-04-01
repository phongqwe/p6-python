from bicp_document_structure.communication.event.P6Event import P6Event
from bicp_document_structure.util.ToException import ToException
from bicp_document_structure.util.ToRepStr import ToRepStr

from bicp_document_structure.util.report.error.ErrorHeader import ErrorHeader
from bicp_document_structure.util.report.error.ErrorReport import ErrorReport

ESErr = "ESErr"


class EventServerErrors:
    class NoReactorReport(ErrorReport):
        header = ErrorHeader(f"{ESErr}1", "no event reactor")

        class Data(ToRepStr):
            def repStr(self) -> str:
                return f"No event reactor for event coded {self._e.code} - {self._e.name}"

            def __init__(self, event: P6Event):
                self._e = event

        def __init__(self, p6Event: P6Event):
            super().__init__(
                header = EventServerErrors.NoReactorReport.header,
                data = EventServerErrors.NoReactorReport.Data(p6Event)
            )