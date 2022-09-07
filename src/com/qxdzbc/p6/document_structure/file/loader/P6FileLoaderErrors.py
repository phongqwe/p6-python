import json
from pathlib import Path

from com.qxdzbc.p6.document_structure.util.report.error.ErrorHeader import ErrorHeader

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
            def __str__(self):
                return json.dumps({
                    "path":str(self.path)
                })

    class FileNotExist:
        header = ErrorHeader(errPrefix() + "3", "file does not exist")

        class Data:
            def __init__(self, path: Path, exception: Exception = None):
                self.path: Path = path
                self.exception: Exception = exception
            def __str__(self):
                return json.dumps({
                    "path":str(self.path)
                })

    class UnableToOpenFile:
        header = ErrorHeader(errPrefix() + "0", "unable to open file")

        class Data:
            def __init__(self, path: Path, exception: Exception = None):
                self.path: Path = path
                self.exception: Exception = exception
            def __str__(self):
                return json.dumps({
                    "path":str(self.path)
                })

    class UnableToReadFile:
        header = ErrorHeader(errPrefix() + "1", "unable to read file")

        class Data:
            def __init__(self, path: Path, exception: Exception = None):
                self.path: Path = path
                self.exception: Exception = exception
            def __str__(self):
                return json.dumps({
                    "path":str(self.path)
                })
