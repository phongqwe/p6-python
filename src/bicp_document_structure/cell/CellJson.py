import json

from bicp_document_structure.cell.address.CellAddressJson import CellAddressJson


class CellJson(dict):
    """
    Json representation of a cell
    """

    def __init__(self, value: str, script: str, address: CellAddressJson):
        super().__init__()
        self.value = value
        self.script = script
        self.addr = (address.col, address.row)

    def __str__(self):
        return json.dumps(self.__dict__)
