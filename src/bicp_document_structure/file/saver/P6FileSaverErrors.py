from pathlib import Path
from typing import Optional

from bicp_document_structure.util.report.error.ErrorHeader import ErrorHeader
from bicp_document_structure.util.report.error.ErrorReport import ErrorReport

__errPrefix = "p6FileSaverError"


def errPrefix():
    return __errPrefix


class P6FileSaverErrors:
    class UnableToAccessPath:
        header = ErrorHeader(errPrefix() + "0", "unable to access path")

        class Data:
            def __init__(self, path: Path, exception: Exception = None):
                self.path: Path = path
                self.exception: Exception = exception

    class UnableToWriteFile:
        header = ErrorHeader(errPrefix() + "1", "unable to write file")

        class Data:
            def __init__(self, path: Path, exception: Exception = None):
                self.path: Path = path
                self.exception: Exception = exception

    @staticmethod
    def toException(errorReport: ErrorReport) -> Optional[Exception]:
        if errorReport.header == P6FileSaverErrors.UnableToAccessPath.header \
                or errorReport.header == P6FileSaverErrors.UnableToAccessPath.header:
            return ValueError(
                "{hd}\n{dt}".format(
                    hd=str(errorReport.header),
                    dt=str(errorReport.data.path)
                )
            )
        else:
            return None
