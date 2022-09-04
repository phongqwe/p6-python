import json
from typing import Union

from com.qxdzbc.p6.document_structure.cell.address.CellAddressJson import CellAddressJson
from com.qxdzbc.p6.document_structure.util.ToJson import ToJson


class CellJson(dict, ToJson):
    """
    Json facade for Cell,
    contains methods to produce a representing json string, and to parse json string into a Cell
    """

    def __init__(self,
                 value: Union[str, None],
                 script: Union[str, None],
                 formula: Union[str, None],
                 address: Union[CellAddressJson, None]):
        super().__init__()
        self.value:Union[str, None] = value
        self.script:Union[str, None] = script
        self.formula:Union[str, None] = formula
        self.address:Union[CellAddressJson, None] = address

    @staticmethod
    def fromJsonDict(jsonDict: dict):
        return CellJson(
            value=jsonDict.get("value"),
            script=jsonDict.get("script"),
            formula=jsonDict.get("formula"),
            address=CellAddressJson.fromJsonDict(jsonDict["address"])
        )

    @staticmethod
    def fromJsonStr(jsonStr: str):
        d = json.loads(jsonStr)
        return CellJson.fromJsonDict(d)

    def __str__(self):
        return json.dumps(self.toJsonDict())

    def toJsonDict(self):
        return {
            "value": self.value,
            "script": self.script,
            "formula":self.formula,
            "address": self.address.__dict__
        }
        # dict = self.__dict__
        # dict["address"] = self.address.__dict__
        # return dict
    def toJsonStr(self) -> str:
        return str(self)
