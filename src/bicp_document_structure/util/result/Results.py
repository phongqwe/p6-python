from bicp_document_structure.report.error.ErrorReports import ErrorReports
from bicp_document_structure.util.result.Result import Result


class Results:
    @staticmethod
    def extractOrRaise(result:Result):
        """extract the value or raise the err as an error"""
        if result.isOk():
            return result.value()
        else:
            raise ErrorReports.toException(result.err())