from typing import Any

from bicp_document_structure.util.ToJson import ToJson
from bicp_document_structure.util.report.error.ErrorHeader import ErrorHeader


class ErrorReport:
    def __init__(self,header:ErrorHeader, data:Any|ToJson, loc:str=""):
        self.header =header
        self.data =data
        self.loc = loc
    def toException(self):
        exceptionObject = self.data
        if isinstance(self.data,ToJson):
            exceptionObject = self.data.toJsonDict()
        return Exception(exceptionObject)