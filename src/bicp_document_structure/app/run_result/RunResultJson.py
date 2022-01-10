from typing import List

from bicp_document_structure.cell.CellJson import CellJson


class RunResultJson(dict):
    """
    Json representation of a RunResult
    """

    def __init__(self, cellJsons:List[CellJson]):
        super().__init__()
        self.cells = cellJsons


