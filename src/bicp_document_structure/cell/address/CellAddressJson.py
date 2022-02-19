import json

from bicp_document_structure.common.ToJsonStr import ToJson


class CellAddressJson(ToJson):
    """
    a json representation of a cell
    """

    def __init__(self, col: int, row: int):
        self.row = row
        self.col = col

    def toJsonDict(self) -> dict:
        return self.__dict__

    def __str__(self):
        return self.toJsonStr()

    def __eq__(self, other):
        if isinstance(other, CellAddressJson):
            return self.row == other.row and self.col == other.col
        else:
            return False

    @staticmethod
    def fromJson(jsonStr: str):
        d = json.loads(jsonStr)
        return CellAddressJson.fromJsonDict(d)

    @staticmethod
    def fromJsonDict(jsonDict: dict):
        return CellAddressJson(
            col = jsonDict.get("col"),
            row = jsonDict.get("row")
        )
