from typing import Optional

from bicp_document_structure.app.errors.AppErrors import AppErrors
from bicp_document_structure.file.loader.P6FileLoaderErrors import P6FileLoaderErrors
from bicp_document_structure.file.saver.P6FileSaverErrors import P6FileSaverErrors
from bicp_document_structure.report.error.ErrorReport import ErrorReport
from bicp_document_structure.util.Util import default
from bicp_document_structure.workbook.WorkbookErrors import WorkbookErrors


class ErrorReports:
    """converterFunction are function that accepts an ErrorReport and returns an Exception or None"""
    converterFunctions = [
        AppErrors.toException,
        P6FileSaverErrors.toException,
        P6FileLoaderErrors.toException,
        WorkbookErrors.toException,
    ]
    @staticmethod
    def toException(errorReport:ErrorReport)->Exception:
        """convert error report to exception"""
        exception = None
        for converterFunction in ErrorReports.converterFunctions:
            exception:Optional[Exception] = converterFunction(errorReport)
            if exception is not None:
                break
        return default(exception,Exception("Unknown error"))