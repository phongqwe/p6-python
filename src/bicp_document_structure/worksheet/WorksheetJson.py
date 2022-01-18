import json
from typing import List

from bicp_document_structure.cell.CellJson import CellJson


class WorksheetJson(dict):
    def __init__(self, name:str,cellJsons:List[CellJson]):
        super().__init__()
        self.name=name
        self.cells = []
        for cell in cellJsons:
            self.cells.append(cell.__dict__)
    def __str__(self):
        return json.dumps(self.__dict__)
