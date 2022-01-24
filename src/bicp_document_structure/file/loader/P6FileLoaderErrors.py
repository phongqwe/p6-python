from pathlib import Path

from bicp_document_structure.error.ErrorHeader import ErrorHeader

__errPrefix = "p6FileLoaderError_"

def errPrefix():
    return __errPrefix

class P6FileLoaderErrors:
    class FileNotExist:
        header = ErrorHeader(errPrefix() + "3", "file does not exist")
        class Data:
            def __init__(self, path: Path, exception: Exception = None):
                self.path: Path = path
                self.exception: Exception = exception
    class UnableToOpenFile:
        header = ErrorHeader(errPrefix() + "0", "unable to open file")
        class Data:
            def __init__(self, path: Path, exception: Exception=None):
                self.path: Path = path
                self.exception: Exception = exception
    class UnableToReadFile:
        header = ErrorHeader(errPrefix() + "1", "unable to read file")
        class Data:
            def __init__(self, path: Path, exception:Exception = None):
                self.path: Path = path
                self.exception:Exception = exception
