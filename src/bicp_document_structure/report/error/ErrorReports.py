from bicp_document_structure.app.errors.AppErrors import AppErrors
from bicp_document_structure.file.loader.P6FileLoaderErrors import P6FileLoaderErrors
from bicp_document_structure.file.saver.P6FileSaverErrors import P6FileSaverErrors
from bicp_document_structure.report.error.ErrorReport import ErrorReport


class ErrorReports:
    """convert error report to exception"""
    @staticmethod
    def toException(errorReport:ErrorReport)->Exception:
        appException = AppErrors.toException(errorReport)
        if appException is not None:
            return appException

        saveException = P6FileSaverErrors.toException(errorReport)
        if saveException is not None:
            return saveException

        loadException = P6FileLoaderErrors.toException(errorReport)
        if loadException is not None:
            return loadException

        return Exception("Unknown error")