from bicp_document_structure.message.event.P6Event import P6Event
from bicp_document_structure.util.ToRepStr import ToRepStr

from bicp_document_structure.util.report.error.ErrorHeader import ErrorHeader

ESErr = "ESErr"

class EventServerErrors:
    class NoReactor:
        header = ErrorHeader(f"{ESErr}1", "no event reactor")

        class Data(ToRepStr):
            def repStr(self) -> str:
                return f"No event reactor for event coded {self._e.code} - {self._e.name}"

            def __init__(self,event:P6Event):
                self._e = event

    class ExceptionError:
        header = ErrorHeader(f"{ESErr}2", "Exception error")
        class Data(ToRepStr):
            def repStr(self) -> str:
                return  f"Encounter exception: {self._e}"

            def __init__(self,exception:Exception):
                self._e = exception