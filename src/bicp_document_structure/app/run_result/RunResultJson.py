import json
from typing import List

from bicp_document_structure.cell.CellJson import CellJson
from bicp_document_structure.cell.address.CellAddressJson import CellAddressJson


class RunResultJson(dict):
    """
    Json representation of a RunResult
    """
    def __init__(self, mutatedCells:List[CellJson], deletedCells:List[CellAddressJson]):
        super().__init__()
        self.mutatedCells = list(map(lambda e:e.__dict__,mutatedCells))
        self.deletedCells = list(map(lambda e:e.__dict__,deletedCells))

    def __str__(self):
        return json.dumps(self.__dict__)