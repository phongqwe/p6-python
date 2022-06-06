from com.emeraldblast.p6.document_structure.communication.event.data_structure.range_event.RangeId import RangeId
from com.emeraldblast.p6.document_structure.util.report.error.ErrorHeader import ErrorHeader
from com.emeraldblast.p6.document_structure.util.report.error.ErrorReport import ErrorReport

CopyErrorsPrefix = "BE_CopyErrors_"
class CopyErrors:
    @staticmethod
    def UnableToCopyRange(rangeId:RangeId):
        return ErrorReport(
            header = ErrorHeader(
                errorCode = f"{CopyErrorsPrefix}0",
                errorDescription = f"Unable to copy range {rangeId.rangeAddress.label}"
            )
        )
    @staticmethod
    def UnableToPasteRange():
        return ErrorReport(
            header = ErrorHeader(
                errorCode = f"{CopyErrorsPrefix}1",
                errorDescription = f"Unable to paste range from clipboard or the data in clipboard is not a range."
            )
        )