from pathlib import Path

from bicp_document_structure.error.ErrorHeader import ErrorHeader

__errPrefix = "p6FileSaverError"
def errPrefix():
    return __errPrefix
class P6FileSaverErrors:
    class UnableToAccessPath:
        header = ErrorHeader(errPrefix() + "0", "unable to access path")
        class Data:
            def __init__(self, path: Path, exception: Exception=None):
                self.path: Path = path
                self.exception: Exception = exception

    class UnableToWriteFile:
        header = ErrorHeader(errPrefix() + "1", "unable to write file")
        class Data:
            def __init__(self, path: Path, exception: Exception=None):
                self.path: Path = path
                self.exception: Exception = exception