from com.emeraldblast.p6.document_structure.communication.event.P6Event import P6Event
from com.emeraldblast.p6.document_structure.util.ToRepStr import ToRepStr

from com.emeraldblast.p6.document_structure.util.report.error.ErrorHeader import ErrorHeader
from com.emeraldblast.p6.document_structure.util.report.error.ErrorReport import ErrorReport

ESErr = "BE_EventServerErrors_"


class EventServerErrors:
    class NoReactorError:
        header = ErrorHeader(f"{ESErr}1", "no event reactor")

        class Data(ToRepStr):
            def repStr(self) -> str:
                return f"No event reactor for event coded {self._e.code} - {self._e.name}"

            def __init__(self, event: P6Event):
                self._e = event


        @staticmethod
        def report(event: P6Event):
            data = EventServerErrors.NoReactorError.Data(event)
            return ErrorReport(
                header = EventServerErrors.NoReactorError.header.setDescription(str(data)),
                data = data
            )

