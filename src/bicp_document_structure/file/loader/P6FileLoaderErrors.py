from pathlib import Path
from typing import Optional

from bicp_document_structure.util.report.error.ErrorHeader import ErrorHeader
from bicp_document_structure.util.report.error.ErrorReport import ErrorReport

__errPrefix = "p6FileLoaderError_"

def errPrefix():
    return __errPrefix

class P6FileLoaderErrors:
    class AlreadyLoad:
        header = ErrorHeader(errPrefix() + "4", "file already loaded")

        class Data:
            def __init__(self, path: Path, exception: Exception = None):
                self.path: Path = path
                self.exception: Exception = exception

    class FileNotExist:
        header = ErrorHeader(errPrefix() + "3", "file does not exist")

        class Data:
            def __init__(self, path: Path, exception: Exception = None):
                self.path: Path = path
                self.exception: Exception = exception

    class UnableToOpenFile:
        header = ErrorHeader(errPrefix() + "0", "unable to open file")

        class Data:
            def __init__(self, path: Path, exception: Exception = None):
                self.path: Path = path
                self.exception: Exception = exception

    class UnableToReadFile:
        header = ErrorHeader(errPrefix() + "1", "unable to read file")

        class Data:
            def __init__(self, path: Path, exception: Exception = None):
                self.path: Path = path
                self.exception: Exception = exception

    @staticmethod
    def toException(errorReport: ErrorReport) -> Optional[Exception]:
        if errorReport.header == P6FileLoaderErrors.AlreadyLoad.header \
                or errorReport.header == P6FileLoaderErrors.FileNotExist.header\
                or errorReport.header == P6FileLoaderErrors.UnableToReadFile.header\
                or errorReport.header == P6FileLoaderErrors.UnableToOpenFile.header:
            return ValueError(
                "{hd}\n{dt}".format(
                    hd=str(errorReport.header),
                    dt=str(errorReport.data.path)
                )
            )
        else:
            return None