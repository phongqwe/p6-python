import json

from bicp_document_structure.common.ToJsonStr import ToJson
from bicp_document_structure.worksheet.WorksheetJson import WorksheetJson


class WorkbookJson(ToJson):

    def __init__(self, name: str, path: str | None, worksheetJsons: list[WorksheetJson]):
        self.name: str = name
        self.path: str | None = path
        self.worksheets: list[WorksheetJson] = worksheetJsons

    def __str__(self):
        return json.dumps(self.toJsonDict())

    def toJsonDict(self) -> dict:
        """convert this object into a dict"""
        worksheets = []
        for sheetJson in self.worksheets:
            sheetDict = sheetJson.toJsonDict()
            worksheets.append(sheetDict)
        return {
            "name": self.name,
            "path": self.path,
            "worksheets": worksheets
        }

    def toJsonDictForSaving(self) -> dict:
        """convert this object into a dict"""
        d = self.toJsonDict()
        d["path"] = None
        return d

    def toJsonStrForSaving(self) -> str:
        return json.dumps(self.toJsonDictForSaving())

    @staticmethod
    def fromJsonDict(jsonDict: dict):
        """create an instance of this class from a dict"""
        worksheetJsons = []
        for sheetDict in jsonDict.get("worksheets"):
            sheetJson = WorksheetJson.fromJsonDict(sheetDict)
            worksheetJsons.append(sheetJson)
        return WorkbookJson(
            name = jsonDict.get("name"),
            path = jsonDict.get("path"),
            worksheetJsons = worksheetJsons
        )

    @staticmethod
    def fromJsonStr(jsonStr: str):
        """create an instance of this class from a json string"""
        d = json.loads(jsonStr)
        return WorkbookJson.fromJsonDict(d)
