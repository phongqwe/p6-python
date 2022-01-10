from typing import List

from bicp_document_structure.cell.CellJson import CellJson


class CompResultJson(dict):
    """
    Json representation of a CompResult
    """

    def __init__(self, cellJsons:List[CellJson]):
        super().__init__()
        self.cells = cellJsons


