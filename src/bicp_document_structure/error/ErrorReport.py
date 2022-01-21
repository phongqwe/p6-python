from typing import Any

from bicp_document_structure.error.ErrorHeader import ErrorHeader


class ErrorReport:
    def __init__(self,header:ErrorHeader, data:Any, loc:str):
        self.header =header
        self.data =data
        self.loc = loc