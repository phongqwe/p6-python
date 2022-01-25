from pathlib import Path

from bicp_document_structure.error.ErrorHeader import ErrorHeader

__errPrefix = "appErrors_"

def errPrefix():
    return __errPrefix

class AppErrors:
    class WorkbookNotExist:
        header = ErrorHeader(errPrefix() + "0", "workbook does not exist")
        class Data:
            def __init__(self, workbookName:str=None,workbookPath:Path=None, index:int=None, exception: Exception = None):
                self.name: str = workbookName
                self.index = index
                self.path = workbookPath
                self.exception: Exception = exception
