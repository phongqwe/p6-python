from com.qxdzbc.p6.document_structure.app.R import R

from com.qxdzbc.p6.document_structure.communication.event.data_structure.range_event.RangeId import RangeId
from com.qxdzbc.p6.document_structure.util.CommonError import CommonErrors
from com.qxdzbc.p6.document_structure.util.report.error.ErrorHeader import ErrorHeader
from com.qxdzbc.p6.document_structure.util.report.error.ErrorReport import ErrorReport

CopyErrorsPrefix = "BE_CopyErrors_"


class CopyPasteErrors:
    class UnableToCopyRange:

        @staticmethod
        def report(rangeId: RangeId):
            return ErrorReport(
                header = ErrorHeader(
                    errorCode = f"{CopyErrorsPrefix}0",
                    errorDescription = f"Unable to copy range {rangeId.rangeAddress.label}"
                )
            )

    class UnableToPasteRange:
        @staticmethod
        def report(e: Exception | None = None):
            if e is None:
                return ErrorReport(
                    header = ErrorHeader(
                        errorCode = f"{CopyErrorsPrefix}1",
                        errorDescription = f"Unable to paste range from clipboard or the data in clipboard is not a range."
                    )
                )
            else:
                return CommonErrors.ExceptionErrorReport.report(e)

    class CantPasteBecauseDataLargerThanSheetLimit:
        @staticmethod
        def report(colCount:int, rowCount:int, colLimit:int, rowLimit:int):
            msg=f"The input data larger than worksheet limit."
            if colCount > colLimit:
                msg = msg+f"\nColumn limit is {colLimit} while the data has {colCount} column."
            if rowCount > rowLimit:
                msg = msg + f"\nRow limit is {rowLimit} while the data has {rowLimit} row."
            return ErrorReport(
                header = ErrorHeader(
                    errorCode = f"{CopyErrorsPrefix}2",
                    errorDescription = msg
                )
            )
    class CantPasteBecauseDataIsLargerThanDestinationRange:
        @staticmethod
        def report(colCount: int, rowCount: int, colLimit: int, rowLimit: int):
            msg = f"The input data is larger the destination range."
            if colCount > colLimit:
                msg = msg + f"\nThe range can hold maximum {colLimit} columns while the data has {colCount} column."
            if rowCount > rowLimit:
                msg = msg + f"\nThe range can hold maximum  {rowLimit} rows while the data has {rowLimit} row."
            return ErrorReport(
                header = ErrorHeader(
                    errorCode = f"{CopyErrorsPrefix}3",
                    errorDescription = msg
                )
            )