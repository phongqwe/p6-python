from com.emeraldblast.p6.document_structure.util.report.error.ErrorHeader import ErrorHeader
from com.emeraldblast.p6.document_structure.util.report.error.ErrorReport import ErrorReport

ESErr = "BE_EventReactorErrors_"

class EventReactorErrors:
    class UnableToParseInput:
        header = ErrorHeader(f"{ESErr}1", "unable to parse input into ")

        @staticmethod
        def report(typeName: str):
            return ErrorReport(
                header = EventReactorErrors.UnableToParseInput.header.concatDescription(typeName),
            )