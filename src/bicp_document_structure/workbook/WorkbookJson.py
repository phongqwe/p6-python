import json
from typing import List, Union

from bicp_document_structure.worksheet.WorksheetJson import WorksheetJson


class WorkbookJson(dict):
    def __init__(self,name:str,path:Union[str,None],worksheetJsons:List[WorksheetJson]):
        super().__init__()
        self.name=name
        self.path=path
        self.worksheets = []
        for sheet in worksheetJsons:
            self.worksheets.append(sheet.__dict__)
    def __str__(self):
        return json.dumps(self.__dict__)