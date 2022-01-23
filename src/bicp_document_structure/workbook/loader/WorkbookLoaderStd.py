import json
from pathlib import Path
from types import SimpleNamespace
from typing import Union

from bicp_document_structure.util.result.Err import Err
from bicp_document_structure.util.result.Result import Result
from bicp_document_structure.workbook.WorkbookJson import WorkbookJson
from bicp_document_structure.workbook.loader.WorkbookLoader import WorkbookLoader


class WorkbookLoaderStd(WorkbookLoader):
    def load(self,filePath:Union[str,Path])->Result:
        path = Path(filePath)
        try:
            file = open(filePath,"r")
            try:
                fileContent = file.read()
                wbJson:WorkbookJson = json.loads(fileContent,object_hook=lambda d: SimpleNamespace(**d))



            except:
                return Err()
        except:
            return Err()