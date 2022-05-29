import json
from pathlib import Path

from com.emeraldblast.p6.document_structure.util.report.error.ErrorHeader import ErrorHeader
from com.emeraldblast.p6.document_structure.util.report.error.ErrorReport import ErrorReport
from com.emeraldblast.p6.document_structure.workbook.key.WorkbookKey import WorkbookKey

__errPrefix = "BE_P6FileSaverErrors_"


def errPrefix():
    return __errPrefix


class P6FileSaverErrors:
    class UnableToAccessPath:
        header = ErrorHeader(errPrefix() + "0", "unable to access path")

        class Data:
            def __init__(self, path: Path, exception: Exception = None):
                self.path: Path = path
                self.exception: Exception = exception

            def __str__(self):
                return json.dumps({
                    "path": str(self.path)
                })

    class UnableToWriteFile:
        header = ErrorHeader(errPrefix() + "1", "unable to write file")

        class Data:
            def __init__(self, path: Path, exception: Exception = None):
                self.path: Path = path
                self.exception: Exception = exception

            def __str__(self):
                return json.dumps({
                    "path": str(self.path)
                })
    class InvalidPath:
        @staticmethod
        def errorReport(workbookKey:WorkbookKey):
            return ErrorReport(
                header=ErrorHeader(
                    f"{errPrefix()}2", f"Can't save workbook {workbookKey.fileName} because the provided path is invalid/None"
                ),
                data = workbookKey
            )

