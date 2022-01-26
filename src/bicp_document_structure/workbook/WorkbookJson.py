import json
from typing import List

from bicp_document_structure.worksheet.WorksheetJson import WorksheetJson


class WorkbookJson(dict):
    def __init__(self, name: str, worksheetJsons: List[WorksheetJson]):
        super().__init__()
        # self.name: str = name
        self.worksheets: List[WorksheetJson] = worksheetJsons

    def __str__(self):
        return json.dumps(self.toJsonDict())

    def toJsonDict(self):
        worksheets = []
        for sheetJson in self.worksheets:
            sheetDict = sheetJson.toJsonDict()
            worksheets.append(sheetDict)
        return {
            # "name": self.name,
            "worksheets": worksheets
        }

    @staticmethod
    def fromJsonDict(jsonDict: dict):
        worksheetJsons = []
        for sheetDict in jsonDict.get("worksheets"):
            sheetJson = WorksheetJson.fromJsonDict(sheetDict)
            worksheetJsons.append(sheetJson)
        return WorkbookJson(
            name=jsonDict.get("name"),
            worksheetJsons=worksheetJsons
        )

    @staticmethod
    def fromJsonStr(jsonStr: str):
        d = json.loads(jsonStr)
        return WorkbookJson.fromJsonDict(d)
