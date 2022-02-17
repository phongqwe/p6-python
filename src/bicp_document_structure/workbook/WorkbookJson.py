import json

from bicp_document_structure.worksheet.WorksheetJson import WorksheetJson


class WorkbookJson(dict):
    def __init__(self, name: str, worksheetJsons: list[WorksheetJson]):
        super().__init__()
        self.name=name
        self.worksheets: list[WorksheetJson] = worksheetJsons

    def __str__(self):
        return json.dumps(self.toJsonDict())

    def toJsonDict(self):
        """convert this object into a dict"""
        worksheets = []
        for sheetJson in self.worksheets:
            sheetDict = sheetJson.toJsonDict()
            worksheets.append(sheetDict)
        return {
            "name":self.name,
            "worksheets": worksheets
        }

    @staticmethod
    def fromJsonDict(jsonDict: dict):
        """create an instance of this class from a dict"""
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
        """create an instance of this class from a json string"""
        d = json.loads(jsonStr)
        return WorkbookJson.fromJsonDict(d)
